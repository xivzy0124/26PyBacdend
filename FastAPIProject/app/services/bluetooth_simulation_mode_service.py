from __future__ import annotations

from threading import Lock

from app.models.schemas import BluetoothSimulationMode, HarmonyAppWebSocketMessage, now_timestamp_ms


class BluetoothSimulationModeService:
    """蓝牙模拟模式：演示兜底。打开后鸿蒙端伪造蓝牙已连接并接管蓝牙压力数据，
    只影响蓝牙数据与连接显示状态，不改动渲染模式本身。"""

    def __init__(self) -> None:
        self._current_mode = BluetoothSimulationMode.OFF
        self._lock = Lock()

    def get_current_mode(self) -> BluetoothSimulationMode:
        with self._lock:
            return self._current_mode

    def update_mode(self, mode_code: str | None) -> BluetoothSimulationMode:
        next_mode = BluetoothSimulationMode.from_code(mode_code)
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
                self._build_option(BluetoothSimulationMode.OFF),
                self._build_option(BluetoothSimulationMode.BLANK),
                self._build_option(BluetoothSimulationMode.STANDING),
                self._build_option(BluetoothSimulationMode.WALKING),
            ],
        }

    def build_mode_changed_message(self) -> HarmonyAppWebSocketMessage:
        mode = self.get_current_mode()
        mode_label = self._get_label(mode)
        mode_description = self._get_description(mode)
        return HarmonyAppWebSocketMessage(
            type="bluetooth_simulation_mode_changed",
            message=f"Bluetooth simulation mode switched to {mode_label}",
            timestamp=now_timestamp_ms(),
            bluetoothSimulationMode=mode.value,
            bluetoothSimulationModeLabel=mode_label,
            bluetoothSimulationModeDescription=mode_description,
        )

    def _build_option(self, mode: BluetoothSimulationMode) -> dict[str, str]:
        return {
            "mode": mode.value,
            "modeLabel": self._get_label(mode),
            "modeDescription": self._get_description(mode),
        }

    @staticmethod
    def _get_label(mode: BluetoothSimulationMode) -> str:
        if mode == BluetoothSimulationMode.BLANK:
            return "模拟空白"
        if mode == BluetoothSimulationMode.STANDING:
            return "模拟站立"
        if mode == BluetoothSimulationMode.WALKING:
            return "模拟走路"
        return "关闭模拟"

    @staticmethod
    def _get_description(mode: BluetoothSimulationMode) -> str:
        if mode == BluetoothSimulationMode.BLANK:
            return "伪造蓝牙已连接但不点亮任何点位（双脚承重为 0），用于演示空白/无响应状态。"
        if mode == BluetoothSimulationMode.STANDING:
            return "伪造蓝牙已连接，模拟站立数据：双脚脚跟 4 点 + 前掌 8 点稳定承重，带轻微体态摆动。"
        if mode == BluetoothSimulationMode.WALKING:
            return "伪造蓝牙已连接，模拟走路数据：左右脚步态错相，重心从脚跟滚动到前掌，足弓留空。"
        return "关闭模拟，使用真实蓝牙压力数据与连接状态。"
