import asyncio
import grpc
import sys
import os
import logging
import argparse

from .server import EmulatorServer

from .proto import emulator_pb2 as pb2

# see https://github.com/grpc/grpc/issues/29459#issuecomment-1641587881
proto_dir = os.path.dirname(pb2.__file__)
sys.path.append(proto_dir)

from .proto import emulator_pb2_grpc  # noqa E402

logger = logging.getLogger(__name__)


async def start(port: int) -> grpc.aio.Server:
    server = grpc.aio.server()
    emulator_pb2_grpc.add_SfpEmulatorServiceServicer_to_server(EmulatorServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    return server


async def _main(port: int) -> None:
    server = await start(port)
    try:
        logger.info(f"Server started on port {port}")
        await server.wait_for_termination()
    except asyncio.CancelledError:
        logger.info("Server is shutting down due to KeyboardInterrupt...")
        await server.stop(grace=10)


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
        asyncio.run(_main(args.port))
    except KeyboardInterrupt:
        logger.info("Server interrupted by user, shutting down...")
