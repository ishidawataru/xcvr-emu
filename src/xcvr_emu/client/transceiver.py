import logging
from typing import Generator

from xcvr_emu.cli import Context, Command
from xcvr_emu.proto import emulator_pb2 as pb2
from xcvr_emu.eeprom import CmisMemMap, XcvrEEPROM


stdout = logging.getLogger("stdout")
stderr = logging.getLogger("stderr")


class TransceiverCommand(Command):
    @property
    def conn(self):
        return self.context.root().conn

    @property
    def eeprom(self):
        return self.context.eeprom

    @property
    def read(self):
        return self.context.read

    @property
    def write(self):
        return self.context.write

    @property
    def mem_map(self):
        return self.context.mem_map


def atoi(l, default=0):
    if len(l) == 0:
        return default
    return int(l[0], 0)


def print_field(field, prefix):
    for k, v in field.items():
        if type(v) is dict:
            stdout.info(f"{prefix}{k}:")
            print_field(v, prefix + "  ")
        else:
            stdout.info(f"{prefix}{k}: {v}")


class Read(TransceiverCommand):
    def __init__(self, context, parent, name, **options):
        super().__init__(context, parent, name, **options)
        self._arguments = []
        self.renamed = {}
        for key in self.mem_map._get_all_fields().keys():
            if " " in key:
                new = key.replace(" ", "-")
                self.renamed[new] = key
                self._arguments.append(new)
            else:
                self._arguments.append(key)

    def arguments(self):
        return self._arguments

    def exec(self, line):
        if len(line) == 0:
            stderr.info("No field specified")
            return
        name = line[0]
        try:
            (page, offset) = name.split(":")
            page = int(page, 0)
            offset = int(offset, 0)
            v = self.read(pb2.ReadRequest(page=page, offset=offset, length=1))
            stdout.info(f"{name}: {v.data[0]:0b}")
            return
        except ValueError:
            pass

        if name in self.renamed:
            name = self.renamed[name]

        try:
            field = self.mem_map.get_field(name)
        except AttributeError:
            stderr.info(f"Unknown field: {name}")
            return
        field = self.eeprom.read(name)
        print_field({name: field}, "")


class ReadRaw(TransceiverCommand):
    def exec(self, line):
        if len(line) == 0:
            stderr.info("No field specified")
            return
        name = line[0]
        (page, offset) = name.split(":")
        page = int(page, 0)
        offset = int(offset, 0)
        v = self.read(pb2.ReadRequest(page=page, offset=offset, length=1))
        stdout.info(f"{name}: {v.data[0]:0b}")


class Write(TransceiverCommand):
    def __init__(self, context, parent, name, **options):
        super().__init__(context, parent, name, **options)
        self._arguments = []
        self.renamed = {}
        for key in self.mem_map._get_all_fields().keys():
            if " " in key:
                new = key.replace(" ", "-")
                self.renamed[new] = key
                self._arguments.append(new)
            else:
                self._arguments.append(key)

    def arguments(self):
        return self._arguments

    def exec(self, line):
        if len(line) < 2:
            stderr.info("Not enough arguments")
            return

        name = line[0]
        if name in self.renamed:
            name = self.renamed[name]

        try:
            self.mem_map.get_field(name)
        except AttributeError:
            stderr.info(f"Unknown field: {name}")
            return
        self.eeprom.write(name, int(line[1], 0))
        return


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
                    f"    DPID: {dpsm.dpid}, Active AppSel: {dpsm.appsel}, State: {dpsm.state}"
                )


class TransceiverContext(Context):
    def __init__(self, parent, index):
        super().__init__(parent, fuzzy_completion=True)
        self.index = index

        mem_map = CmisMemMap()

        self.mem_map = mem_map

        self.eeprom = XcvrEEPROM(index, parent.conn, mem_map)

        self.read = self.parent.conn.Read
        self.write = self.parent.conn.Write

        self.add_command("read", Read)
        self.add_command("read-raw", ReadRaw)
        self.add_command("write", Write)
        self.add_command("remove", Remove)
        self.add_command("insert", Insert)
        self.add_command("info", Info)

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
