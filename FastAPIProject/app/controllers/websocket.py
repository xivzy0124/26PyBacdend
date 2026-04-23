from __future__ import annotations

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.container import get_container_from_websocket
from app.models.schemas import HarmonyAppWebSocketMessage, now_timestamp_ms

router = APIRouter()


@router.websocket("/ws/harmony-app")
async def harmony_app_socket(websocket: WebSocket) -> None:
    container = get_container_from_websocket(websocket)
    await websocket.accept()
    session_id = container.connection_manager.register(websocket)

    try:
        await websocket.send_json(
            container.ai_mode_service.build_mode_changed_message().model_dump(exclude_none=True)
        )
        while True:
            payload_text = await websocket.receive_text()
            heartbeat_reply = build_heartbeat_ack(payload_text)
            if heartbeat_reply is None:
                continue
            await websocket.send_json(heartbeat_reply.model_dump(exclude_none=True))
    except WebSocketDisconnect:
        pass
    finally:
        container.connection_manager.unregister(session_id)


def build_heartbeat_ack(payload_text: str) -> HarmonyAppWebSocketMessage | None:
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, dict):
        return None

    payload_type = payload.get("type")
    if payload_type != "heartbeat":
        return None

    return HarmonyAppWebSocketMessage(
        type="heartbeat_ack",
        message="pong",
        timestamp=now_timestamp_ms(),
    )
