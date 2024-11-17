import sys
import os
import traceback
import asyncio
import logging

from .xcvr import CMISTransceiver

from .proto import emulator_pb2 as pb2

# see https://github.com/grpc/grpc/issues/29459#issuecomment-1641587881
proto_dir = os.path.dirname(pb2.__file__)
sys.path.append(proto_dir)

from .proto import emulator_pb2_grpc  # noqa E402

logger = logging.getLogger(__name__)


class EmulatorServer(emulator_pb2_grpc.SfpEmulatorService):
    def __init__(self):
        super().__init__()
        self.xcvrs = {}
        self.monitors = []

    async def Read(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
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

    async def Write(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]
        data = req.data
        logger.debug(
            f"write: bank: {req.bank}, page: {req.page:02X}h, offset: {req.offset}, length: {req.length}, data: {data if len(data) > 1 else bin(data[0])}"
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

    async def GetInfo(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]
        dpsms = [
            pb2.DataPathStateMachine(
                dpid=v._dpid, appsel=v._appsel, state=str(v._state)
            )
            for v in xcvr._dpsms.values()
        ]
        return pb2.GetInfoResponse(present=xcvr.present, dpsms=dpsms)

    async def UpdateInfo(self, req, context):
        if req.index not in self.xcvrs:
            self.xcvrs[req.index] = CMISTransceiver(req.index)
        xcvr = self.xcvrs[req.index]
        if req.present:
            await xcvr.plugin()
        else:
            await xcvr.plugout()

        return pb2.UpdateInfoResponse()

    async def notify_monitors(self, message):
        for queue in self.monitors:
            await queue.put(message)

    async def Monitor(self, request, context):
        queue = asyncio.Queue()
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

    async def List(self, req, context):
        infos = []
        for k, v in self.xcvrs.items():
            info = pb2.GetInfoResponse()
            info.index = k
            info.present = v.present
            infos.append(info)

        return pb2.ListResponse(infos=infos)