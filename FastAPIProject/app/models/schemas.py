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
    mode: str | None = None
    modeLabel: str | None = None
    modeDescription: str | None = None
