from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse

from app.container import AppContainer, get_container_from_request
from app.models.schemas import ApiResponse, BubbleMessageRequest
from app.views.ws_control_page import render_ws_control_page

router = APIRouter()


@router.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/ws-control.html", status_code=307)


@router.get("/ws-control.html", response_class=HTMLResponse, include_in_schema=False)
async def ws_control_page() -> HTMLResponse:
    return HTMLResponse(render_ws_control_page())


@router.get("/api/ws/harmony/status", response_model=ApiResponse)
async def get_harmony_ws_status(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    connected_clients = container.connection_manager.get_connected_count()
    data = {
        "connectedClients": connected_clients,
        "webSocketPath": "/ws/harmony-app",
        "controlPage": "/ws-control.html",
    }
    return ApiResponse.success(data)


@router.post("/api/ws/harmony/notify-connected", response_model=ApiResponse)
async def notify_connected(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_connection_success_notification()
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "connection success notification sent"
        if delivered_count > 0
        else "no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/ws/harmony/notify-message", response_model=ApiResponse)
async def notify_message(
    request: BubbleMessageRequest,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    message_text = request.message.strip()
    if message_text == "":
        return ApiResponse.error(400, "message cannot be empty")

    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_app_bubble(message_text)
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "message": message_text,
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "app bubble notification sent"
        if delivered_count > 0
        else "no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/ws/harmony/notify-tts", response_model=ApiResponse)
async def notify_tts(
    request: BubbleMessageRequest,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    message_text = request.message.strip()
    if message_text == "":
        return ApiResponse.error(400, "message cannot be empty")

    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_app_tts(message_text)
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "message": message_text,
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "app tts notification sent"
        if delivered_count > 0
        else "no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.get("/api/ai/mode", response_model=ApiResponse)
async def get_ai_mode(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.ai_mode_service.build_mode_payload())


@router.post("/api/ai/mode", response_model=ApiResponse)
async def update_ai_mode(
    mode: str = Query(..., description="模式代码：mode1/mode2/mode3"),
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        container.ai_mode_service.update_mode(mode)
        mode_payload = container.ai_mode_service.build_mode_payload()
        broadcast_message = container.ai_mode_service.build_mode_changed_message()
        await container.connection_manager.broadcast(broadcast_message)
        return ApiResponse.success(mode_payload, broadcast_message.message)
    except ValueError as error:
        return ApiResponse.error(400, str(error))
