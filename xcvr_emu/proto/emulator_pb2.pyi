"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class ReadRequest(google.protobuf.message.Message):
    """ReadRequest"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    BANK_FIELD_NUMBER: builtins.int
    PAGE_FIELD_NUMBER: builtins.int
    OFFSET_FIELD_NUMBER: builtins.int
    LENGTH_FIELD_NUMBER: builtins.int
    FORCE_FIELD_NUMBER: builtins.int
    index: builtins.int
    bank: builtins.int
    page: builtins.int
    offset: builtins.int
    length: builtins.int
    """Length"""
    force: builtins.bool
    """return value even if not present"""
    def __init__(
        self,
        *,
        index: builtins.int = ...,
        bank: builtins.int = ...,
        page: builtins.int = ...,
        offset: builtins.int = ...,
        length: builtins.int = ...,
        force: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["bank", b"bank", "force", b"force", "index", b"index", "length", b"length", "offset", b"offset", "page", b"page"]) -> None: ...

global___ReadRequest = ReadRequest

@typing.final
class ReadResponse(google.protobuf.message.Message):
    """ReadResponse"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    data: builtins.bytes
    """Data"""
    def __init__(
        self,
        *,
        data: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["data", b"data"]) -> None: ...

global___ReadResponse = ReadResponse

@typing.final
class WriteRequest(google.protobuf.message.Message):
    """WriteRequest"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    BANK_FIELD_NUMBER: builtins.int
    PAGE_FIELD_NUMBER: builtins.int
    OFFSET_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    LENGTH_FIELD_NUMBER: builtins.int
    index: builtins.int
    bank: builtins.int
    page: builtins.int
    offset: builtins.int
    data: builtins.bytes
    """Data"""
    length: builtins.int
    def __init__(
        self,
        *,
        index: builtins.int = ...,
        bank: builtins.int = ...,
        page: builtins.int = ...,
        offset: builtins.int = ...,
        data: builtins.bytes = ...,
        length: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["bank", b"bank", "data", b"data", "index", b"index", "length", b"length", "offset", b"offset", "page", b"page"]) -> None: ...

global___WriteRequest = WriteRequest

@typing.final
class WriteResponse(google.protobuf.message.Message):
    """WriteResponse"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___WriteResponse = WriteResponse

@typing.final
class GetInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    index: builtins.int
    def __init__(
        self,
        *,
        index: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["index", b"index"]) -> None: ...

global___GetInfoRequest = GetInfoRequest

@typing.final
class DataPathStateMachine(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DPID_FIELD_NUMBER: builtins.int
    APPSEL_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    dpid: builtins.int
    appsel: builtins.int
    state: builtins.str
    def __init__(
        self,
        *,
        dpid: builtins.int = ...,
        appsel: builtins.int = ...,
        state: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["appsel", b"appsel", "dpid", b"dpid", "state", b"state"]) -> None: ...

global___DataPathStateMachine = DataPathStateMachine

@typing.final
class ModuleState(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STATE_FIELD_NUMBER: builtins.int
    VENDOR_NAME_FIELD_NUMBER: builtins.int
    state: builtins.str
    vendor_name: builtins.str
    def __init__(
        self,
        *,
        state: builtins.str = ...,
        vendor_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["state", b"state", "vendor_name", b"vendor_name"]) -> None: ...

global___ModuleState = ModuleState

@typing.final
class GetInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PRESENT_FIELD_NUMBER: builtins.int
    INDEX_FIELD_NUMBER: builtins.int
    MSM_FIELD_NUMBER: builtins.int
    DPSMS_FIELD_NUMBER: builtins.int
    present: builtins.bool
    index: builtins.int
    @property
    def msm(self) -> global___ModuleState: ...
    @property
    def dpsms(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DataPathStateMachine]: ...
    def __init__(
        self,
        *,
        present: builtins.bool = ...,
        index: builtins.int = ...,
        msm: global___ModuleState | None = ...,
        dpsms: collections.abc.Iterable[global___DataPathStateMachine] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["msm", b"msm"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["dpsms", b"dpsms", "index", b"index", "msm", b"msm", "present", b"present"]) -> None: ...

global___GetInfoResponse = GetInfoResponse

@typing.final
class UpdateInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    PRESENT_FIELD_NUMBER: builtins.int
    index: builtins.int
    present: builtins.bool
    def __init__(
        self,
        *,
        index: builtins.int = ...,
        present: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["index", b"index", "present", b"present"]) -> None: ...

global___UpdateInfoRequest = UpdateInfoRequest

@typing.final
class UpdateInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UpdateInfoResponse = UpdateInfoResponse

@typing.final
class MonitorRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    index: builtins.int
    """0 to monitor all"""
    def __init__(
        self,
        *,
        index: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["index", b"index"]) -> None: ...

global___MonitorRequest = MonitorRequest

@typing.final
class MonitorResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    BANK_FIELD_NUMBER: builtins.int
    PAGE_FIELD_NUMBER: builtins.int
    OFFSET_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    LENGTH_FIELD_NUMBER: builtins.int
    PRESENT_FIELD_NUMBER: builtins.int
    WRITE_FIELD_NUMBER: builtins.int
    index: builtins.int
    bank: builtins.int
    page: builtins.int
    offset: builtins.int
    data: builtins.bytes
    length: builtins.int
    present: builtins.bool
    write: builtins.bool
    """true: write, false: read"""
    def __init__(
        self,
        *,
        index: builtins.int = ...,
        bank: builtins.int = ...,
        page: builtins.int = ...,
        offset: builtins.int = ...,
        data: builtins.bytes = ...,
        length: builtins.int = ...,
        present: builtins.bool = ...,
        write: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["bank", b"bank", "data", b"data", "index", b"index", "length", b"length", "offset", b"offset", "page", b"page", "present", b"present", "write", b"write"]) -> None: ...

global___MonitorResponse = MonitorResponse

@typing.final
class ListRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ListRequest = ListRequest

@typing.final
class ListResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFOS_FIELD_NUMBER: builtins.int
    @property
    def infos(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GetInfoResponse]: ...
    def __init__(
        self,
        *,
        infos: collections.abc.Iterable[global___GetInfoResponse] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["infos", b"infos"]) -> None: ...

global___ListResponse = ListResponse
