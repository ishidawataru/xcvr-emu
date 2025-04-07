import asyncio
import logging

import pytest
import pytest_asyncio
import importlib.resources
import yaml

from cmis import MemMap, LanesEnum
from xcvr_emu.proto.emulator_pb2 import ReadRequest, WriteRequest
from xcvr_emu.transceiver import CMISTransceiver

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def xcvr(caplog):
    caplog.set_level(logging.INFO)

    with importlib.resources.open_text("xcvr_emu", "config.yaml") as f:
        config = yaml.safe_load(f)
        config = config["transceivers"][0]

    xcvr = CMISTransceiver(0, config)
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
        req = WriteRequest(
            index=0, bank=bank, offset=offset, page=page, length=length, data=data
        )
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


@pytest.mark.asyncio
async def test_dpsm_activation(caplog, xcvr: CMISTransceiver):

    m = MemMap(remote=MemoryAccessor(xcvr))

    m.LowPwrRequestSW.value = m.LowPwrRequestSW.NO_REQUEST

    await asyncio.sleep(0.1)

    assert m.ModuleState.value == m.ModuleState.MODULE_READY
    assert m.ApplicationDescriptor[0].HostLaneCount.value == LanesEnum.FOUR_LANES

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPACTIVATED
        assert m.DPStateHostLane[i + 4].value == m.DPStateHostLane.DPDEACTIVATED

    for deinit in m.DPDeinitLane:
        assert deinit.value == deinit.INITIALIZE

    for i in range(4):
        m.DPDeinitLane[i].lvalue = m.DPDeinitLane.DEINITIALIZE
    m.DPDeinitLane.store()

    await asyncio.sleep(0.1)

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPDEACTIVATED

    for i in range(4):
        m.DPDeinitLane[i].lvalue = m.DPDeinitLane.INITIALIZE
    m.DPDeinitLane.store()

    await asyncio.sleep(0.1)

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPACTIVATED


@pytest.mark.asyncio
async def test_dpsm_output_disable_handling(caplog, xcvr: CMISTransceiver):

    m = MemMap(remote=MemoryAccessor(xcvr))

    for output in m.OutputDisableTx:
        output.value = output.DISABLED

    m.LowPwrRequestSW.value = m.LowPwrRequestSW.NO_REQUEST

    await asyncio.sleep(0.1)

    assert m.ModuleState.value == m.ModuleState.MODULE_READY
    assert m.ApplicationDescriptor[0].HostLaneCount.value == LanesEnum.FOUR_LANES

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPINITIALIZED
        assert m.DPStateHostLane[i + 4].value == m.DPStateHostLane.DPDEACTIVATED

    for output in m.OutputDisableTx:
        output.lvalue = output.ENABLED
    m.OutputDisableTx.store()

    await asyncio.sleep(0.1)

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPACTIVATED

@pytest.mark.asyncio
async def test_dpsm_activation_with_bank(caplog, xcvr: CMISTransceiver):

    m = MemMap(remote=MemoryAccessor(xcvr))

    m.LowPwrRequestSW.value = m.LowPwrRequestSW.NO_REQUEST

    await asyncio.sleep(0.1)

    assert m.ModuleState.value == m.ModuleState.MODULE_READY
    assert m.ApplicationDescriptor[0].HostLaneCount.value == LanesEnum.FOUR_LANES
    assert m.BanksSupported.value == m.BanksSupported.BANKS_0_3_SUPPORTED

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPACTIVATED
        assert m.DPStateHostLane[i + 4].value == m.DPStateHostLane.DPDEACTIVATED

    for deinit in m.DPDeinitLane:
        assert deinit.value == deinit.INITIALIZE

    for i in range(4):
        m.DPDeinitLane[i].lvalue = m.DPDeinitLane.DEINITIALIZE

    m.DPDeinitLane.store()

    await asyncio.sleep(0.1)

    for i in range(4):
        assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPDEACTIVATED

    for bank in range(1, 4):
        m.bank = bank
        for i in range(4):
            assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPACTIVATED

    m.bank = 1
    for i in range(4):
        m.DPDeinitLane[i].lvalue = m.DPDeinitLane.DEINITIALIZE

    m.DPDeinitLane.store()

    await asyncio.sleep(0.1)

    for bank in [0, 1]:
        m.bank = bank
        for i in range(4):
            assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPDEACTIVATED

    for bank in [2, 3]:
        m.bank = bank
        for i in range(4):
            assert m.DPStateHostLane[i].value == m.DPStateHostLane.DPACTIVATED
