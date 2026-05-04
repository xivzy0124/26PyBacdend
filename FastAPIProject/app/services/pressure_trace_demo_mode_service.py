from __future__ import annotations

from threading import Lock

from app.models.schemas import PressureTraceDemoMode, HarmonyAppWebSocketMessage, now_timestamp_ms


class PressureTraceDemoModeService:
    def __init__(self) -> None:
        self._current_mode = PressureTraceDemoMode.NORMAL
        self._lock = Lock()

    def get_current_mode(self) -> PressureTraceDemoMode:
        with self._lock:
            return self._current_mode

    def update_mode(self, mode_code: str | None) -> PressureTraceDemoMode:
        next_mode = PressureTraceDemoMode.from_code(mode_code)
        with self._lock:
            self._current_mode = next_mode
        return next_mode

    def build_mode_payload(self) -> dict[str, object]:
        mode = self.get_current_mode()
        return {
            "mode": mode.value,
            "modeLabel": self._get_label(mode),
            "modeDescription": self._get_description(mode),
            "availableModes": [
                self._build_option(PressureTraceDemoMode.NORMAL),
                self._build_option(PressureTraceDemoMode.JITTER),
            ],
        }

    def build_mode_changed_message(self) -> HarmonyAppWebSocketMessage:
        mode = self.get_current_mode()
        mode_label = self._get_label(mode)
        mode_description = self._get_description(mode)
        return HarmonyAppWebSocketMessage(
            type="pressure_trace_demo_mode_changed",
            message=f"Pressure trace demo mode switched to {mode_label}",
            timestamp=now_timestamp_ms(),
            pressureTraceMode=mode.value,
            pressureTraceModeLabel=mode_label,
            pressureTraceModeDescription=mode_description,
        )

    def _build_option(self, mode: PressureTraceDemoMode) -> dict[str, str]:
        return {
            "mode": mode.value,
            "modeLabel": self._get_label(mode),
            "modeDescription": self._get_description(mode),
        }

    @staticmethod
    def _get_label(mode: PressureTraceDemoMode) -> str:
        if mode == PressureTraceDemoMode.JITTER:
            return "轨迹波动"
        return "轨迹正常"

    @staticmethod
    def _get_description(mode: PressureTraceDemoMode) -> str:
        if mode == PressureTraceDemoMode.JITTER:
            return "只放大重心轨迹的时间片错位，模拟左右脚独立设备数据不同步导致的异常跳变。"
        return "重心轨迹按左右脚最新实时数据正常合成显示，不影响其他足压卡片。"
