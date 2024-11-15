from xcvr_emu.xcvr_emud import EmulatorServer

from xcvr_emu.proto.emulator_pb2 import ReadRequest, WriteRequest

import pytest

import pytest_asyncio


@pytest_asyncio.fixture
async def server():
    return EmulatorServer()


@pytest.mark.asyncio
async def test_Read(server):
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    res = await server.Read(req, None)
    assert res.data == bytearray([0x0])


@pytest.mark.asyncio
async def test_Write(server):
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1, force=True)
    res = await server.Read(req, None)
    assert res.data == bytearray([0x18])

    req = WriteRequest(index=0, bank=0, offset=0, page=0, length=1, data=bytes([0xAA]))
    await server.Write(req, None)

    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1, force=True)
    res = await server.Read(req, None)
    assert res.data == bytearray([0xAA])
