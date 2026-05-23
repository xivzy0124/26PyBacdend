from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


def now_local() -> datetime:
    return datetime.now()


def now_timestamp_ms() -> int:
    return int(datetime.now().timestamp() * 1000)


class AiMode(str, Enum):
    MODE1 = "mode1"
    MODE2 = "mode2"
    MODE3 = "mode3"

    @classmethod
    def from_code(cls, code: str | None) -> "AiMode":
        if code is None or code.strip() == "":
            return cls.MODE1
        for mode in cls:
            if mode.value == code.strip().lower():
                return mode
        raise ValueError(f"Unsupported ai mode: {code}")


class PressureDemoMode(str, Enum):
    EMPTY = "empty"
    DIRECT = "direct"
    REPAIR = "repair"

    @classmethod
    def from_code(cls, code: str | None) -> "PressureDemoMode":
        if code is None or code.strip() == "":
            return cls.DIRECT
        for mode in cls:
            if mode.value == code.strip().lower():
                return mode
        raise ValueError(f"Unsupported pressure demo mode: {code}")


class PressureTraceDemoMode(str, Enum):
    NORMAL = "normal"
    JITTER = "jitter"

    @classmethod
    def from_code(cls, code: str | None) -> "PressureTraceDemoMode":
        if code is None or code.strip() == "":
            return cls.NORMAL
        for mode in cls:
            if mode.value == code.strip().lower():
                return mode
        raise ValueError(f"Unsupported pressure trace demo mode: {code}")


class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any | None = None
    timestamp: datetime

    @classmethod
    def success(cls, data: Any | None = None, message: str = "success") -> "ApiResponse":
        return cls(code=200, message=message, data=data, timestamp=now_local())

    @classmethod
    def error(cls, code: int, message: str, data: Any | None = None) -> "ApiResponse":
        return cls(code=code, message=message, data=data, timestamp=now_local())


class HarmonyAppWebSocketMessage(BaseModel):
    type: str
    message: str
    timestamp: int
    audioUrl: str | None = None
    audioContentType: str | None = None
    mode: str | None = None
    modeLabel: str | None = None
    modeDescription: str | None = None
    postureDemoMode: str | None = None
    postureDemoTitle: str | None = None
    postureDemoPhase: str | None = None
    postureDemoBodyDetected: bool | None = None
    postureDemoTrackingReady: bool | None = None
    postureDemoCameraActive: bool | None = None
    postureDemoLocked: bool | None = None
    postureDemoReload: bool | None = None
    demoPostureMode: str | None = None
    demoPostureTitle: str | None = None
    demoPosturePhase: str | None = None
    demoPostureBodyDetected: bool | None = None
    demoPostureTrackingReady: bool | None = None
    demoPostureCameraActive: bool | None = None
    demoPostureAutoNavigate: bool | None = None
    pressureDemoMode: str | None = None
    pressureDemoModeLabel: str | None = None
    pressureDemoModeDescription: str | None = None
    pressureTraceMode: str | None = None
    pressureTraceModeLabel: str | None = None
    pressureTraceModeDescription: str | None = None
    aiCoachAction: str | None = None
    aiCoachVideoUrl: str | None = None
    aiCoachLoop: bool | None = None
    aiCoachReturnToIdle: bool | None = None
    aiCoachAudioDurationMs: int | None = None


class BubbleMessageRequest(BaseModel):
    message: str


class PostureDemoCommandRequest(BaseModel):
    action: str


class AiCoachActionRequest(BaseModel):
    action: str


class OnlineTtsRequest(BaseModel):
    message: str
    vcn: str | None = None


class LibraryAudioPlayRequest(BaseModel):
    filename: str


class LibraryAudioPromoteRequest(BaseModel):
    filename: str


class XfyunTtsAccountUpsertRequest(BaseModel):
    accountId: str | None = None
    name: str
    appId: str
    apiKey: str
    apiSecret: str
    defaultVcn: str = "xiaoyan"
    description: str | None = None
    enabled: bool = True


class XfyunTtsAccountView(BaseModel):
    accountId: str
    name: str
    appId: str
    apiKey: str
    apiSecret: str
    defaultVcn: str
    description: str
    enabled: bool
    isActive: bool
    updatedAt: datetime


class XfyunTtsAccountSelectRequest(BaseModel):
    accountId: str
