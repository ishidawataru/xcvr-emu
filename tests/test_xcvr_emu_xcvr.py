from xcvr_emu.xcvr import CMISTransceiver

from xcvr_emu.proto.emulator_pb2 import ReadRequest, WriteRequest

import pytest
import pytest_asyncio


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
