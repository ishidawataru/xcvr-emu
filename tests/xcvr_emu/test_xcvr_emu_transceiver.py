import asyncio
import logging

import pytest
import pytest_asyncio

from cmis import MemMap
from xcvr_emu.proto.emulator_pb2 import ReadRequest, WriteRequest
from xcvr_emu.transceiver import CMISTransceiver

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def xcvr(caplog):
    caplog.set_level(logging.INFO)
    xcvr = CMISTransceiver(0)
    await xcvr.plugin()
    yield xcvr
    await xcvr.plugout()


@pytest.mark.asyncio
async def test_read(xcvr):
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    assert xcvr.read(req) == bytes([0x18])  # QSFP-DD


@pytest.mark.asyncio
async def test_write(xcvr):
    req = WriteRequest(index=0, bank=0, offset=0, page=0, length=1, data=bytes([0xAA]))
    xcvr.write(req)
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    assert xcvr.read(req) == bytes([0xAA])

class MemoryAccessor:
    def __init__(self, xcvr: CMISTransceiver):
        self.xcvr = xcvr

    def read(self, bank: int, page: int, offset: int, length: int) -> bytes:
        req = ReadRequest(index=0, bank=bank, offset=offset, page=page, length=length)
        return self.xcvr.read(req)

    def write(
        self, bank: int, page: int, offset: int, length: int, data: bytes
    ) -> None:
        req = WriteRequest(index=0, bank=bank, offset=offset, page=page, length=length, data=data)
        self.xcvr.write(req)



@pytest.mark.asyncio
async def test_lowpwr_handling(caplog, xcvr: CMISTransceiver):

    m = MemMap(remote=MemoryAccessor(xcvr))

    assert m.ModuleState.value == m.ModuleState.MODULE_LOW_PWR
    assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.LOW_POWER_MODE

    m.LowPwrRequestSW.value = m.LowPwrRequestSW.NO_REQUEST

    await asyncio.sleep(0.1)

    assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.NO_REQUEST
    assert m.ModuleState.value == m.ModuleState.MODULE_READY

    m.LowPwrRequestSW.value = m.LowPwrRequestSW.LOW_POWER_MODE

    await asyncio.sleep(0.1)

    assert m.ModuleState.value == m.ModuleState.MODULE_LOW_PWR
    assert m.LowPwrRequestSW.value == m.LowPwrRequestSW.LOW_POWER_MODE
