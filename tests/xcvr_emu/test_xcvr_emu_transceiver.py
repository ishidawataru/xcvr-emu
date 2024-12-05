import asyncio
import logging

import pytest
import pytest_asyncio

from cmis import ModuleState
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
    assert await xcvr.read(req) == bytearray([0x18])  # QSFP-DD


@pytest.mark.asyncio
async def test_write(xcvr):
    req = WriteRequest(index=0, bank=0, offset=0, page=0, length=1, data=bytes([0xAA]))
    await xcvr.write(req)
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    assert await xcvr.read(req) == bytearray([0xAA])


@pytest.mark.asyncio
async def test_lowpwr_handling(caplog, xcvr: CMISTransceiver):
    assert xcvr._state == ModuleState.MODULE_LOW_PWR

    low_pwr_req = xcvr.mem_map.LowPwrRequestSW
    res = await xcvr.read(ReadRequest(offset=low_pwr_req.address.offset, length=1))
    assert ((res[0] >> low_pwr_req.address.bit) & 1) == low_pwr_req.LOW_POWER_MODE.value

    await xcvr.write(
        WriteRequest(offset=low_pwr_req.address.offset, length=1, data=bytes([0]))
    )

    await asyncio.sleep(0.1)

    low_pwr_req = xcvr.mem_map.LowPwrRequestSW
    res = await xcvr.read(ReadRequest(offset=low_pwr_req.address.offset, length=1))
    assert ((res[0] >> low_pwr_req.address.bit) & 1) == low_pwr_req.NO_REQUEST.value

    assert xcvr._state == ModuleState.MODULE_READY

    data: int = res[0] | (low_pwr_req.LOW_POWER_MODE.value << low_pwr_req.address.bit)

    await xcvr.write(
        WriteRequest(
            offset=low_pwr_req.address.offset, length=1, data=data.to_bytes(1, "big")
        )
    )

    await asyncio.sleep(0.1)

    assert xcvr._state == ModuleState.MODULE_LOW_PWR
