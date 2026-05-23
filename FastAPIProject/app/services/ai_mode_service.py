from __future__ import annotations

from threading import Lock

from app.models.schemas import AiMode, HarmonyAppWebSocketMessage, now_timestamp_ms


class AiModeService:
    def __init__(self) -> None:
        self._current_mode = AiMode.MODE2
        self._lock = Lock()

    def get_current_mode(self) -> AiMode:
        with self._lock:
            return self._current_mode

    def update_mode(self, mode_code: str | None) -> AiMode:
        next_mode = AiMode.from_code(mode_code)
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
                self._build_option(AiMode.MODE1),
                self._build_option(AiMode.MODE2),
                self._build_option(AiMode.MODE3),
            ],
        }

    def build_mode_changed_message(self) -> HarmonyAppWebSocketMessage:
        mode = self.get_current_mode()
        mode_label = self._get_label(mode)
        mode_description = self._get_description(mode)
        return HarmonyAppWebSocketMessage(
            type="ai_mode_changed",
            message=f"AI mode switched to {mode_label}",
            timestamp=now_timestamp_ms(),
            mode=mode.value,
            modeLabel=mode_label,
            modeDescription=mode_description,
        )

    def _build_option(self, mode: AiMode) -> dict[str, str]:
        return {
            "mode": mode.value,
            "modeLabel": self._get_label(mode),
            "modeDescription": self._get_description(mode),
        }

    @staticmethod
    def _get_label(mode: AiMode) -> str:
        if mode == AiMode.MODE1:
            return "正常"
        if mode == AiMode.MODE2:
            return "非正常"
        if mode == AiMode.MODE3:
            return "非正常扩展"
        return "正常"

    @staticmethod
    def _get_description(mode: AiMode) -> str:
        if mode == AiMode.MODE1:
            return "正常样本会输出完整的技能加载、脚本执行与标准分析结果。"
        if mode == AiMode.MODE2:
            return "当前默认展示的是非正常样本分析流式输出。"
        if mode == AiMode.MODE3:
            return "保留另一组非正常样本流式输出。"
        return "正常样本会输出完整的技能加载、脚本执行与标准分析结果。"
