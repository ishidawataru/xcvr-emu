from xcvr_emu.xcvr_emud import EmulatorServer

from xcvr_emu.proto.emulator_pb2 import (
    ReadRequest,
    WriteRequest,
    ListRequest,
    ListResponse,
    DeleteRequest,
)

import pytest
import importlib.resources

import pytest_asyncio


@pytest_asyncio.fixture
async def server():
    with importlib.resources.open_text("xcvr_emu", "config.yaml") as f:
        async with EmulatorServer(f.name) as server:
            yield server


@pytest.mark.asyncio
async def test_List(server: EmulatorServer) -> None:
    req = ListRequest()
    res: ListResponse = await server.List(req, None)
    assert len(res.infos) == 9
    assert res.infos[0].index == 0


@pytest.mark.asyncio
async def test_Delete(server: EmulatorServer) -> None:
    await server.Delete(DeleteRequest(index=0), None)

    req = ListRequest()
    res: ListResponse = await server.List(req, None)
    assert len(res.infos) == 8


@pytest.mark.asyncio
async def test_Read(server):
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1)
    res = await server.Read(req, None)
    assert res.data == bytes([0x18])


@pytest.mark.asyncio
async def test_Write(server):
    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1, force=True)
    res = await server.Read(req, None)
    assert res.data == bytes([0x18])

    req = WriteRequest(index=0, bank=0, offset=0, page=0, length=1, data=bytes([0xAA]))
    await server.Write(req, None)

    req = ReadRequest(index=0, bank=0, offset=0, page=0, length=1, force=True)
    res = await server.Read(req, None)
    assert res.data == bytes([0xAA])
