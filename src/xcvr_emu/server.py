import asyncio
import logging
import os
import sys
import traceback
from typing import AsyncGenerator

import grpc

from .proto import emulator_pb2 as pb2
from .transceiver import CMISTransceiver

# see https://github.com/grpc/grpc/issues/29459#issuecomment-1641587881
proto_dir = os.path.dirname(pb2.__file__)
sys.path.append(proto_dir)

from .proto import emulator_pb2_grpc  # noqa E402

logger = logging.getLogger(__name__)


class EmulatorServer(emulator_pb2_grpc.SfpEmulatorServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.xcvrs: dict[int, CMISTransceiver] = {}
        self.monitors: list[asyncio.Queue] = []

    async def __aenter__(self):
        return self

    async def stop(self):
        logger.info("Stopping emulator server")
        for xcvr in self.xcvrs.values():
            await xcvr.plugout()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.stop()

    async def Create(self, req: pb2.CreateRequest, context) -> pb2.CreateResponse:
        if req.index in self.xcvrs:
            raise grpc.RpcError(
                grpc.StatusCode.ALREADY_EXISTS,
                f"Transceiver({req.index}) already exists",
            )

        xcvr = CMISTransceiver(req.index)
        self.xcvrs[req.index] = xcvr

        return pb2.CreateResponse()

    async def Delete(self, req: pb2.DeleteRequest, context) -> pb2.DeleteResponse:
        if req.index not in self.xcvrs:
            raise grpc.RpcError(
                grpc.StatusCode.NOT_FOUND, f"Transceiver({req.index}) does not exist"
            )

        xcvr = self.xcvrs.pop(req.index)
        await xcvr.plugout()

        return pb2.DeleteResponse()

    async def Read(self, req: pb2.ReadRequest, context) -> pb2.ReadResponse:
        if req.index not in self.xcvrs:
            raise grpc.RpcError(
                grpc.StatusCode.NOT_FOUND, f"Transceiver({req.index}) does not exist"
            )

        xcvr = self.xcvrs[req.index]
        data = bytes(await xcvr.read(req))

        await self.notify_monitors(
            {
                "index": req.index,
                "bank": req.bank,
                "page": req.page,
                "offset": req.offset,
                "data": data,
                "length": req.length,
                "present": xcvr.present,
                "write": False,
            }
        )

        return pb2.ReadResponse(data=data)

    async def Write(self, req: pb2.WriteRequest, context) -> pb2.WriteResponse:
        if req.index not in self.xcvrs:
            raise grpc.RpcError(
                grpc.StatusCode.NOT_FOUND, f"Transceiver({req.index}) does not exist"
            )

        xcvr = self.xcvrs[req.index]
        data = req.data
        logger.debug(
            f"write: bank: {req.bank}, page: {req.page:02X}h, offset: {req.offset}, length: {req.length}, data: {data if len(data) > 1 else bin(data[0])!r}"
        )

        try:
            await xcvr.write(req)
        except Exception as e:
            logger.error(f"Error writing to EEPROM: {e}")
            traceback.print_exc()
            raise e from None

        await self.notify_monitors(
            {
                "index": req.index,
                "bank": req.bank,
                "page": req.page,
                "offset": req.offset,
                "data": req.data,
                "length": req.length,
                "present": xcvr.present,
                "write": True,
            }
        )

        return pb2.WriteResponse()

    async def GetInfo(self, req: pb2.GetInfoRequest, context) -> pb2.GetInfoResponse:
        if req.index not in self.xcvrs:
            raise grpc.RpcError(
                grpc.StatusCode.NOT_FOUND, f"Transceiver({req.index}) does not exist"
            )

        xcvr = self.xcvrs[req.index]
        dpsms = [
            pb2.DataPathStateMachine(
                dpid=v._dpid, appsel=v._appsel, state=str(v._state)
            )
            for v in xcvr._dpsms.values()
        ]
        return pb2.GetInfoResponse(present=xcvr.present, dpsms=dpsms)

    async def UpdateInfo(self, req: pb2.UpdateInfoRequest, context) -> pb2.UpdateInfoResponse:
        if req.index not in self.xcvrs:
            raise grpc.RpcError(
                grpc.StatusCode.NOT_FOUND, f"Transceiver({req.index}) does not exist"
            )

        xcvr = self.xcvrs[req.index]
        if req.present:
            await xcvr.plugin()
        else:
            await xcvr.plugout()

        return pb2.UpdateInfoResponse()

    async def notify_monitors(self, message):
        for queue in self.monitors:
            await queue.put(message)

    async def Monitor(self, request: pb2.MonitorRequest, context) -> AsyncGenerator[pb2.MonitorResponse, None]:
        queue: asyncio.Queue = asyncio.Queue()
        self.monitors.append(queue)

        index = request.index

        try:
            while True:
                message = await queue.get()
                if index and message["index"] != index:
                    continue
                yield pb2.MonitorResponse(**message)
        except asyncio.CancelledError:
            pass
        finally:
            self.monitors.remove(queue)

    async def List(self, req: pb2.ListRequest, context) -> pb2.ListResponse:
        infos = []
        for k, v in self.xcvrs.items():
            info = pb2.GetInfoResponse()
            info.index = k
            info.present = v.present
            infos.append(info)

        return pb2.ListResponse(infos=infos)
