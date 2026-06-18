from __future__ import annotations

from fastapi import Request, WebSocket

from app.services.ai_mode_service import AiModeService
from app.core.config import settings
from app.services.connection_manager import HarmonyConnectionManager
from app.services.pressure_demo_mode_service import PressureDemoModeService
from app.services.pressure_trace_demo_mode_service import PressureTraceDemoModeService
from app.services.bluetooth_simulation_mode_service import BluetoothSimulationModeService
from app.services.xfyun_online_tts_service import XfyunOnlineTtsService
from app.services.xfyun_tts_account_service import XfyunTtsAccountService


class AppContainer:
    def __init__(self) -> None:
        self.ai_mode_service = AiModeService()
        self.connection_manager = HarmonyConnectionManager()
        self.pressure_demo_mode_service = PressureDemoModeService()
        self.pressure_trace_demo_mode_service = PressureTraceDemoModeService()
        self.bluetooth_simulation_mode_service = BluetoothSimulationModeService()
        self.xfyun_tts_account_service = XfyunTtsAccountService()
        self.bt_online_tts_service = XfyunOnlineTtsService(
            self.xfyun_tts_account_service,
            audio_cache_dir=settings.bt_cache_dir,
            audio_library_dir=settings.bt_library_dir,
            audio_cache_url_prefix="/bt_cache",
            audio_library_url_prefix="/bt_library",
        )
        self.cp_online_tts_service = XfyunOnlineTtsService(
            self.xfyun_tts_account_service,
            audio_cache_dir=settings.cp_cache_dir,
            audio_library_dir=settings.cp_library_dir,
            audio_cache_url_prefix="/cp_cache",
            audio_library_url_prefix="/cp_library",
        )
        self.ai_online_tts_service = XfyunOnlineTtsService(
            self.xfyun_tts_account_service,
            audio_cache_dir=settings.ai_cache_dir,
            audio_library_dir=settings.ai_library_dir,
            audio_cache_url_prefix="/ai_cache",
            audio_library_url_prefix="/ai_library",
        )


def get_container_from_request(request: Request) -> AppContainer:
    return request.app.state.container


def get_container_from_websocket(websocket: WebSocket) -> AppContainer:
    return websocket.app.state.container
