import logging

import pytest

from xcvr_emu.proto.emulator_pb2 import CreateRequest, GetInfoRequest, UpdateInfoRequest
from xcvr_emu.xcvr_emud import Emud


@pytest.mark.asyncio
async def test_emud_lifetime(caplog):
    caplog.set_level(logging.DEBUG)
    async with Emud(50051) as emud:
        req = CreateRequest(index=0)
        await emud.emulator.Create(req, None)

        req = UpdateInfoRequest(index=0, present=True)
        await emud.emulator.UpdateInfo(req, None)

        req = GetInfoRequest(index=0)
        res = await emud.emulator.GetInfo(req, None)

        assert res.present

    assert "Transceiver(0) started" in caplog.text
    assert "Transceiver(0) task cancelled" in caplog.text
    assert "Stopping emulator server" in caplog.text
