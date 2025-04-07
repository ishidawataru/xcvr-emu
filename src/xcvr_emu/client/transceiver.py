import logging
from typing import Generator

from xcvr_emu.cli import Command, Context
from cmis import Address, MemMap, Field
from xcvr_emu.proto import emulator_pb2 as pb2

stdout = logging.getLogger("stdout")
stderr = logging.getLogger("stderr")


class TransceiverCommand(Command):
    @property
    def conn(self):
        return self.context.root().conn

    @property
    def read(self):
        return self.context.read

    @property
    def write(self):
        return self.context.write

    @property
    def mem_map(self):
        return self.context.mem_map

    @property
    def bank(self):
        return self.context.bank


class RegisterCommand(TransceiverCommand):
    def __init__(self, context: "BankContext", parent, name, **options):
        super().__init__(context, parent, name, **options)
        self._arguments = []
        for key in self.mem_map.group_map.keys():
            self._arguments.append(key)
        for key in self.mem_map.field_map.keys():
            self._arguments.append(key)

    def arguments(self):
        return self._arguments


class Read(RegisterCommand):
    def exec(self, line):
        if len(line) == 0:
            stderr.info("No field specified")
            return
        name = line[0]

        field = self.mem_map.search_by_name(
            name, include_groups=True, include_fields=True
        )
        if field is None:
            try:
                address = Address.from_str(name)
            except ValueError:
                stderr.info("Usage: read <field> | <address>")
                return
        else:
            address = field.address

        v = self.read(
            bank=self.bank,
            page=address.page,
            offset=address.start_byte,
            length=address.byte_size,
        )

        if field is None:
            for f, v in self.mem_map.decode(address.page, address.start_byte, v):
                stdout.info(f.to_str(value=v))
        else:
            stdout.info(field.to_str(value=v, recursive=True))


class Write(RegisterCommand):
    def exec(self, line):
        if len(line) < 2:
            stderr.info("Not enough arguments")
            return

        name = line[0]

        field = self.mem_map.search_by_name(
            name, include_groups=True, include_fields=True
        )
        if field is None:
            try:
                address = Address.from_str(name)
            except ValueError:
                stderr.info("Usage: read <field> | <address>")
                return
        else:
            address = field.address

        try:
            src_int = int(line[1], 0)
            if address.bit is not None:
                dst = self.read(
                    bank=self.bank,
                    page=address.page,
                    offset=address.start_byte,
                    length=address.byte_size,
                )
                dst_int = int.from_bytes(dst, "big")
                start_bit = address.start_bit % 8

                mask = ((1 << address.size) - 1) << start_bit
                dst_cleared = dst_int & ~mask
                src_shifted = (src_int << start_bit) & mask

                src_int = dst_cleared | src_shifted

            data = src_int.to_bytes(address.byte_size, "big")
        except ValueError:
            stderr.info("Invalid value")
            return

        self.write(
            bank=self.bank,
            page=address.page,
            offset=address.start_byte,
            length=address.byte_size,
            data=data,
        )


class RegInfo(RegisterCommand):
    def exec(self, line):
        if len(line) == 0:
            stderr.info("No field specified")
            return
        name = line[0]

        field = self.mem_map.search_by_name(
            name, include_groups=True, include_fields=True
        )
        if field is None:
            try:
                address = Address.from_str(name)
            except ValueError:
                stderr.info("Usage: read <field> | <address>")
                return
            for f in self.mem_map.search(address.page, address.offset, address.bit):
                stdout.info(f.to_str())
        else:
            stdout.info(field.describe())


class Remove(TransceiverCommand):
    def exec(self, line):
        try:
            req = pb2.UpdateInfoRequest(index=self.context.index, present=False)
        except ValueError as e:
            stderr.info(e)
            return
        self.conn.UpdateInfo(req)


class Insert(TransceiverCommand):
    def exec(self, line):
        try:
            req = pb2.UpdateInfoRequest(index=self.context.index, present=True)
        except ValueError as e:
            stderr.info(e)
            return
        self.conn.UpdateInfo(req)


class Info(TransceiverCommand):
    def exec(self, line):
        try:
            res = self.conn.GetInfo(pb2.GetInfoRequest(index=self.context.index))
        except ValueError as e:
            stderr.info(e)
            return
        stdout.info(f"Transceiver({self.context.index}):")
        stdout.info(f"  present: {res.present}")
        if len(res.dpsms) == 0:
            stdout.info("  No DPSM configured")
        else:
            stdout.info("  DPSM:")
            for dpsm in res.dpsms:
                stdout.info(
                    f"    DPID: {dpsm.bank}:{dpsm.dpid}, Active AppSel: {dpsm.appsel}, State: {dpsm.state}"
                )


class MemoryAccessor:
    def __init__(self, index, conn):
        self.index = index
        self.conn = conn

    def read(self, bank: int, page: int, offset: int, length: int) -> bytes:
        res = self.conn.Read(
            pb2.ReadRequest(
                index=self.index, bank=bank, page=page, offset=offset, length=length
            )
        )
        # stdout.info(f"Read: {bank=}, {page=}, {offset=}, {length=}, {res.data=}")
        return res.data

    def write(
        self, bank: int, page: int, offset: int, length: int, data: bytes
    ) -> None:
        # stdout.info(f"Write: {bank=}, {page=}, {offset=}, {length=}, {data=}")
        self.conn.Write(
            pb2.WriteRequest(
                index=self.index,
                bank=bank,
                page=page,
                offset=offset,
                length=length,
                data=data,
            )
        )


class BankContext(Context):
    def __init__(self, parent, index, bank=0):
        super().__init__(parent, fuzzy_completion=True)
        self.index = index
        self.bank = bank

        acc = MemoryAccessor(index, parent.root().conn)

        self.mem_map = MemMap(acc)

        self.read = acc.read
        self.write = acc.write

        self.add_command("read", Read, no_completion_on_exec=True)
        self.add_command("write", Write, no_completion_on_exec=True)
        self.add_command("reginfo", RegInfo, no_completion_on_exec=True)
        self.add_command("remove", Remove)
        self.add_command("insert", Insert)
        self.add_command("info", Info)

    def __str__(self):
        return f"bank({self.bank})"


class Bank(TransceiverCommand):
    def arguments(self) -> Generator[str, None, None]:
        f: Field = self.mem_map.search_by_name("BanksSupported", include_fields=True)
        v = self.read(
            bank=0,
            page=f.address.page,
            offset=f.address.start_byte,
            length=f.address.byte_size,
        )
        return (str(i) for i in range(2 ** int(v[0])))

    def exec(self, line):
        if not line:
            stderr.error(f"usage: {self.name} <bank>")
            return

        return BankContext(self.context, self.context.index, int(line[0], 0))


class TransceiverContext(BankContext):
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.add_command("bank", Bank)

    def __str__(self):
        return f"transceiver({self.index})"


class Transceiver(Command):
    def arguments(self) -> Generator[str, None, None]:
        res = self.context.conn.List(pb2.ListRequest())
        return (str(info.index) for info in res.infos)

    def exec(self, line):
        if not line:
            stderr.error(f"usage: {self.name} <index>")
            return

        if line[0] not in list(self.arguments()):
            stderr.error(f"Transceiver({line[0]}) does not exist")
            return

        return TransceiverContext(self.context, int(line[0]))
