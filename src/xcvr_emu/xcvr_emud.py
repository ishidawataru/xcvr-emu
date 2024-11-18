import argparse
import asyncio
import logging
import os
import sys

import grpc

from .proto import emulator_pb2 as pb2
from .server import EmulatorServer

# see https://github.com/grpc/grpc/issues/29459#issuecomment-1641587881
proto_dir = os.path.dirname(pb2.__file__)
sys.path.append(proto_dir)

from .proto import emulator_pb2_grpc  # noqa E402

logger = logging.getLogger(__name__)

class Emud:
    def __init__(self, port:int, grace:int=10) -> None:
        self.port = port
        self.grace = grace
        self.server = grpc.aio.server()
        self.emulator = EmulatorServer()
        emulator_pb2_grpc.add_SfpEmulatorServiceServicer_to_server(self.emulator, self.server)
        self.server.add_insecure_port(f"[::]:{port}")

    async def start(self) -> None:
        return await self.server.start()

    async def wait_for_termination(self) -> None:
        await self.server.wait_for_termination()

    async def stop(self, grace: float | None) -> None:
        _raised_exception = None
        try:
            await self.server.stop(grace=grace)
        except asyncio.CancelledError as e:
            _raised_exception = e

        await self.emulator.stop()
        if _raised_exception:
            raise _raised_exception

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.stop(grace=self.grace)




async def _main(port: int) -> None:
    async with Emud(port) as emud:
        logger.info(f"Server started at port {port}")
        await emud.wait_for_termination()


def main():
    argparser = argparse.ArgumentParser(description="Transceiver Emulator Server")
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    argparser.add_argument(
        "-p", "--port", type=int, default=50051, help="Port number to listen"
    )

    args = argparser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    try:
        asyncio.run(_main(args.port), debug=args.verbose)
    except KeyboardInterrupt:
        logger.info("Server intterupted by user, exiting...")
