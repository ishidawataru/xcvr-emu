import argparse
import asyncio
import logging
import os
import sys

import grpc
from prompt_toolkit import PromptSession, patch_stdout

from xcvr_emu.client import Shell
from xcvr_emu.proto import emulator_pb2 as pb2

# see https://github.com/grpc/grpc/issues/29459#issuecomment-1641587881
proto_dir = os.path.dirname(pb2.__file__)
sys.path.append(proto_dir)

from xcvr_emu.proto import emulator_pb2_grpc  # noqa E402


stdout = logging.getLogger("stdout")
stderr = logging.getLogger("stderr")


async def loop_async(shell):
    session = PromptSession()

    with patch_stdout.patch_stdout():
        while True:
            c = shell.completer()
            p = shell.prompt()
            b = shell.bindings()
            session.app.shell = shell
            try:
                line = await session.prompt_async(
                    p, completer=c, key_bindings=b, default=shell.default_input
                )
            except KeyboardInterrupt:
                stderr.info("Execute 'exit' to exit")
                continue

            if len(line) > 0:
                shell.exec(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-c", "--command-string")
    parser.add_argument("-k", "--keep-open", action="store_true")
    parser.add_argument("-x", "--stdin", action="store_true")
    args = parser.parse_args()

    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)-5s][%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger = logging.getLogger("xcvr-emu")
    logger.addHandler(console)
    console.setLevel(logging.DEBUG)  # emit all messages sent to this handler
    v = args.verbose
    if v == 0:
        logger.setLevel(logging.ERROR)
    elif v == 1:
        logger.setLevel(logging.INFO)
    else:  # v > 1
        logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    shf = logging.Formatter("%(message)s")
    sh.setFormatter(shf)

    stdout.setLevel(logging.DEBUG)
    stdout.addHandler(sh)

    sh2 = logging.StreamHandler(sys.stderr)
    sh2.setLevel(logging.DEBUG)
    sh2.setFormatter(shf)

    stderr.setLevel(logging.DEBUG)
    stderr.addHandler(sh2)

    channel = grpc.insecure_channel("localhost:50051")
    conn = emulator_pb2_grpc.SfpEmulatorServiceStub(channel)

    shell = Shell(conn)

    async def _main():
        if args.stdin or args.command_string:
            stream = sys.stdin if args.stdin else args.command_string.split(";")
            for line in stream:
                shell.exec(line)
            if not args.keep_open:
                return

        tasks = [loop_async(shell)]

        await asyncio.gather(*tasks)

    asyncio.run(_main())


if __name__ == "__main__":
    main()
