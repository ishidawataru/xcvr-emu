import logging
from typing import Iterable

from grpc import RpcError

from xcvr_emu.cli import Command, Context
from xcvr_emu.client.transceiver import Transceiver
from xcvr_emu.proto import emulator_pb2 as pb2

stdout = logging.getLogger("stdout")
stderr = logging.getLogger("stderr")

def catch_rpc_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RpcError as e:
            stderr.error(f"RPC Error: {e.code()}: {e.details()}")
    return wrapper



class List(Command):
    @catch_rpc_errors
    def exec(self, line):
        res = self.context.conn.List(pb2.ListRequest())
        for info in res.infos:
            stdout.info(f"{info.index}: present: {info.present}")


class Create(Command):
    @catch_rpc_errors
    def exec(self, line):
        if not line:
            stderr.error(f"usage: {self.name} <index>")
            return

        try:
            req = pb2.CreateRequest(index=int(line[0]))
        except ValueError:
            stderr.error(f"usage: {self.name} <index>")
            return

        self.context.conn.Create(req)

class Delete(Command):
    def arguments(self) -> Iterable[str]:
        try:
            res = self.context.conn.List(pb2.ListRequest())
        except RpcError:
            return iter([])

        return (str(info.index) for info in res.infos)

    @catch_rpc_errors
    def exec(self, line):
        if not line:
            stderr.error(f"usage: {self.name} <index>")
            return

        try:
            req = pb2.DeleteRequest(index=int(line[0]))
        except ValueError:
            stderr.error(f"usage: {self.name} <index>")
            return

        self.context.conn.Delete(req)


class Root(Context):
    def __init__(self, conn):
        super().__init__(None, fuzzy_completion=True)
        self.conn = conn

        self.add_command("list", List)
        self.add_command("create", Create)
        self.add_command("delete", Delete)
        self.add_command("transceiver", Transceiver)

    def __str__(self):
        return ""
