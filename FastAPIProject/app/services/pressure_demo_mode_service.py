from __future__ import annotations

from threading import Lock

from app.models.schemas import PressureDemoMode, HarmonyAppWebSocketMessage, now_timestamp_ms


class PressureDemoModeService:
    def __init__(self) -> None:
        self._current_mode = PressureDemoMode.DIRECT
        self._lock = Lock()

    def get_current_mode(self) -> PressureDemoMode:
        with self._lock:
            return self._current_mode

    def update_mode(self, mode_code: str | None) -> PressureDemoMode:
        next_mode = PressureDemoMode.from_code(mode_code)
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
                self._build_option(PressureDemoMode.EMPTY),
                self._build_option(PressureDemoMode.DIRECT),
                self._build_option(PressureDemoMode.REPAIR),
            ],
        }

    def build_mode_changed_message(self) -> HarmonyAppWebSocketMessage:
        mode = self.get_current_mode()
        mode_label = self._get_label(mode)
        mode_description = self._get_description(mode)
        return HarmonyAppWebSocketMessage(
            type="pressure_demo_mode_changed",
            message=f"Pressure demo mode switched to {mode_label}",
            timestamp=now_timestamp_ms(),
            pressureDemoMode=mode.value,
            pressureDemoModeLabel=mode_label,
            pressureDemoModeDescription=mode_description,
        )

    def _build_option(self, mode: PressureDemoMode) -> dict[str, str]:
        return {
            "mode": mode.value,
            "modeLabel": self._get_label(mode),
            "modeDescription": self._get_description(mode),
        }

    @staticmethod
    def _get_label(mode: PressureDemoMode) -> str:
        if mode == PressureDemoMode.EMPTY:
            return "模式1"
        if mode == PressureDemoMode.REPAIR:
            return "模式3"
        return "模式2"

    @staticmethod
    def _get_description(mode: PressureDemoMode) -> str:
        if mode == PressureDemoMode.EMPTY:
            return "蓝牙双脚连接后维持空白热力图，用于演示无响应阶段。"
        if mode == PressureDemoMode.REPAIR:
            return "蓝牙双脚连接后按真实受力做同区域线性扩散，减少热力图空洞。"
        return "蓝牙双脚连接后按真实落点直接点亮，对应当前实时直出效果。"
