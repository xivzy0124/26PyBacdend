from __future__ import annotations

from fastapi import Request, WebSocket

from app.services.ai_mode_service import AiModeService
from app.services.connection_manager import HarmonyConnectionManager


class AppContainer:
    def __init__(self) -> None:
        self.ai_mode_service = AiModeService()
        self.connection_manager = HarmonyConnectionManager()


def get_container_from_request(request: Request) -> AppContainer:
    return request.app.state.container


def get_container_from_websocket(websocket: WebSocket) -> AppContainer:
    return websocket.app.state.container
