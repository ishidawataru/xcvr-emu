import logging

from xcvr_emu.cli import Context, Command
from xcvr_emu.proto import emulator_pb2 as pb2

from xcvr_emu.client.transceiver import Transceiver

stdout = logging.getLogger("stdout")
stderr = logging.getLogger("stderr")


class List(Command):
    def exec(self, line):
        res = self.context.conn.List(pb2.ListRequest())
        for info in res.infos:
            stdout.info(f"{info.index}: present: {info.present}")


class Root(Context):

    def __init__(self, conn):
        super().__init__(None, fuzzy_completion=True)
        self.conn = conn

        self.add_command("list", List)
        self.add_command("transceiver", Transceiver)

    def __str__(self):
        return ""
