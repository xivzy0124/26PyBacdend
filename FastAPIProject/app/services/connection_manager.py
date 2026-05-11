from __future__ import annotations

from threading import RLock
from uuid import uuid4

from fastapi import WebSocket
from starlette.websockets import WebSocketState

from app.models.schemas import HarmonyAppWebSocketMessage, now_timestamp_ms


class HarmonyConnectionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, WebSocket] = {}
        self._lock = RLock()

    def register(self, websocket: WebSocket) -> str:
        session_id = uuid4().hex[:12]
        with self._lock:
            self._sessions[session_id] = websocket
        return session_id

    def unregister(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)

    def get_connected_count(self) -> int:
        self._cleanup_closed_sessions()
        with self._lock:
            return len(self._sessions)

    async def send_connection_success_notification(self) -> int:
        message = HarmonyAppWebSocketMessage(
            type="connection_success",
            message="连接成功",
            timestamp=now_timestamp_ms(),
        )
        return await self.broadcast(message)

    async def send_app_tts(self, message_text: str) -> int:
        message = HarmonyAppWebSocketMessage(
            type="app_tts",
            message=message_text,
            timestamp=now_timestamp_ms(),
        )
        return await self.broadcast(message)

    async def send_app_bubble(self, message_text: str) -> int:
        message = HarmonyAppWebSocketMessage(
            type="app_bubble",
            message=message_text,
            timestamp=now_timestamp_ms(),
        )
        return await self.broadcast(message)

    async def send_app_audio_play(
        self,
        audio_url: str,
        message_text: str,
        audio_content_type: str = "audio/mpeg",
    ) -> int:
        message = HarmonyAppWebSocketMessage(
            type="app_audio_play",
            message=message_text,
            audioUrl=audio_url,
            audioContentType=audio_content_type,
            timestamp=now_timestamp_ms(),
        )
        return await self.broadcast(message)

    async def send_posture_demo_command(
        self,
        mode: str,
        title: str,
        message_text: str,
        phase: str,
        body_detected: bool,
        tracking_ready: bool,
        camera_active: bool,
        demo_locked: bool,
    ) -> int:
        message = HarmonyAppWebSocketMessage(
            type="posture_demo_control",
            message=message_text,
            timestamp=now_timestamp_ms(),
            postureDemoMode=mode,
            postureDemoTitle=title,
            postureDemoPhase=phase,
            postureDemoBodyDetected=body_detected,
            postureDemoTrackingReady=tracking_ready,
            postureDemoCameraActive=camera_active,
            postureDemoLocked=demo_locked,
        )
        return await self.broadcast(message)

    async def send_posture_demo_reload(self) -> int:
        message = HarmonyAppWebSocketMessage(
            type="posture_demo_reload",
            message="reload posture workbench",
            timestamp=now_timestamp_ms(),
            postureDemoReload=True,
        )
        return await self.broadcast(message)

    async def send_demo_posture_command(
        self,
        mode: str,
        title: str,
        message_text: str,
        phase: str,
        body_detected: bool,
        tracking_ready: bool,
        camera_active: bool,
        auto_navigate: bool,
    ) -> int:
        message = HarmonyAppWebSocketMessage(
            type="demo_posture_control",
            message=message_text,
            timestamp=now_timestamp_ms(),
            demoPostureMode=mode,
            demoPostureTitle=title,
            demoPosturePhase=phase,
            demoPostureBodyDetected=body_detected,
            demoPostureTrackingReady=tracking_ready,
            demoPostureCameraActive=camera_active,
            demoPostureAutoNavigate=auto_navigate,
        )
        return await self.broadcast(message)

    async def send_pressure_demo_mode_changed(
        self,
        mode: str,
        mode_label: str,
        mode_description: str,
    ) -> int:
        message = HarmonyAppWebSocketMessage(
            type="pressure_demo_mode_changed",
            message=f"Pressure demo mode switched to {mode_label}",
            timestamp=now_timestamp_ms(),
            pressureDemoMode=mode,
            pressureDemoModeLabel=mode_label,
            pressureDemoModeDescription=mode_description,
        )
        return await self.broadcast(message)

    async def broadcast(self, message: HarmonyAppWebSocketMessage) -> int:
        self._cleanup_closed_sessions()
        with self._lock:
            session_items = list(self._sessions.items())

        delivered_count = 0
        for session_id, websocket in session_items:
            try:
                await websocket.send_json(message.model_dump(exclude_none=True))
                delivered_count += 1
            except Exception:
                self.unregister(session_id)
        return delivered_count

    def _cleanup_closed_sessions(self) -> None:
        with self._lock:
            closed_ids = [
                session_id
                for session_id, websocket in self._sessions.items()
                if websocket.client_state != WebSocketState.CONNECTED
            ]
            for session_id in closed_ids:
                self._sessions.pop(session_id, None)
