from __future__ import annotations

from fastapi import Request, WebSocket

from app.services.ai_mode_service import AiModeService
from app.services.connection_manager import HarmonyConnectionManager
from app.services.xfyun_online_tts_service import XfyunOnlineTtsService
from app.services.xfyun_tts_account_service import XfyunTtsAccountService


class AppContainer:
    def __init__(self) -> None:
        self.ai_mode_service = AiModeService()
        self.connection_manager = HarmonyConnectionManager()
        self.xfyun_tts_account_service = XfyunTtsAccountService()
        self.xfyun_online_tts_service = XfyunOnlineTtsService(self.xfyun_tts_account_service)


def get_container_from_request(request: Request) -> AppContainer:
    return request.app.state.container


def get_container_from_websocket(websocket: WebSocket) -> AppContainer:
    return websocket.app.state.container
