import asyncio

import pytest
import pytest_asyncio

from xcvr_emu.eeprom import consts
from xcvr_emu.proto.emulator_pb2 import ReadRequest, WriteRequest
from xcvr_emu.transceiver import CMISTransceiver, ModuleGlobalControls


@pytest_asyncio.fixture
async def xcvr():
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
async def test_lowpwr_handling(caplog, xcvr):
    assert xcvr._state == xcvr.State.LowPwr

    field= xcvr.mem_map.get_field(consts.MODULE_LEVEL_CONTROL)
    res = await xcvr.read(ReadRequest(offset=field.offset, length=1))
    assert res == bytearray([ModuleGlobalControls.LowPwrRequestSW.value])

    await xcvr.write(WriteRequest(offset=field.offset, length=1, data=bytes([0])))

    await asyncio.sleep(.1)

    assert xcvr._state == xcvr.State.Ready

    await xcvr.write(WriteRequest(offset=field.offset, length=1, data=bytes([ModuleGlobalControls.LowPwrRequestSW.value])))

    await asyncio.sleep(.1)

    assert xcvr._state == xcvr.State.LowPwr
