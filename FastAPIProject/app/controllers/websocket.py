from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.container import get_container_from_websocket

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
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        container.connection_manager.unregister(session_id)
