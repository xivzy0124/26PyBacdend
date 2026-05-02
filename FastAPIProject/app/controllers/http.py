from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.container import AppContainer, get_container_from_request
from app.core.config import settings
from app.models.schemas import (
    ApiResponse,
    BubbleMessageRequest,
    LibraryAudioPlayRequest,
    OnlineTtsRequest,
    PostureDemoCommandRequest,
)
from app.views.ws_control_page import render_ws_control_page

router = APIRouter()


POSTURE_DEMO_PRESETS: dict[str, dict[str, object]] = {
    "stage1": {
        "mode": "stage1",
        "title": "阶段1",
        "message": "已识别，左侧骨骼正常，右侧模型静止无反馈",
        "phase": "running",
        "bodyDetected": True,
        "trackingReady": False,
        "cameraActive": True,
        "demoLocked": True,
    },
    "stage2": {
        "mode": "stage2",
        "title": "阶段2",
        "message": "左侧骨骼正常，右侧模型动作错乱且无法贴合",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "demoLocked": True,
    },
    "stage3": {
        "mode": "stage3",
        "title": "阶段3",
        "message": "左侧骨骼正常，右侧模型跟随迟缓且明显卡顿",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "demoLocked": True,
    },
    "normal": {
        "mode": "normal",
        "title": "阶段4",
        "message": "恢复正常实时链路",
        "phase": "ready",
        "bodyDetected": False,
        "trackingReady": False,
        "cameraActive": False,
        "demoLocked": False,
    },
    "stage4": {
        "mode": "normal",
        "title": "阶段4",
        "message": "恢复正常实时链路",
        "phase": "ready",
        "bodyDetected": False,
        "trackingReady": False,
        "cameraActive": False,
        "demoLocked": False,
    },
}


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


@router.post("/api/ws/harmony/notify-bubble", response_model=ApiResponse)
async def notify_bubble(
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


@router.post("/api/ws/harmony/posture-demo", response_model=ApiResponse)
async def notify_posture_demo(
    payload: PostureDemoCommandRequest,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    action = payload.action.strip().lower()
    demo_preset = POSTURE_DEMO_PRESETS.get(action)
    if demo_preset is None:
        return ApiResponse.error(400, f"unsupported posture demo action: {payload.action}")

    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_posture_demo_command(
        mode=str(demo_preset["mode"]),
        title=str(demo_preset["title"]),
        message_text=str(demo_preset["message"]),
        phase=str(demo_preset["phase"]),
        body_detected=bool(demo_preset["bodyDetected"]),
        tracking_ready=bool(demo_preset["trackingReady"]),
        camera_active=bool(demo_preset["cameraActive"]),
        demo_locked=bool(demo_preset["demoLocked"]),
    )
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "action": action,
        "mode": demo_preset["mode"],
        "title": demo_preset["title"],
        "message": demo_preset["message"],
        "phase": demo_preset["phase"],
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "posture demo command sent"
        if delivered_count > 0
        else "no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/ws/harmony/posture-demo-reload", response_model=ApiResponse)
async def notify_posture_demo_reload(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_posture_demo_reload()
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "posture demo reload sent"
        if delivered_count > 0
        else "no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.get("/api/tts/online/config", response_model=ApiResponse)
async def get_online_tts_config(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.xfyun_online_tts_service.build_runtime_payload())


@router.get("/api/tts/online/library", response_model=ApiResponse)
async def get_online_tts_library(
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    library_assets = container.xfyun_online_tts_service.list_library_audio_assets()
    data = [
        {
            "filename": asset.filename,
            "displayName": asset.display_name,
            "audioUrl": build_public_asset_url(request, asset.relative_url),
        }
        for asset in library_assets
    ]
    return ApiResponse.success(data)


@router.post("/api/ws/harmony/notify-online-tts", response_model=ApiResponse)
async def notify_online_tts(
    payload: OnlineTtsRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    message_text = payload.message.strip()
    if message_text == "":
        return ApiResponse.error(400, "message cannot be empty")

    try:
        generated_audio = await container.xfyun_online_tts_service.synthesize_to_cache(
            message_text=message_text,
            vcn=(payload.vcn or "").strip() or None,
        )
    except ValueError as error:
        return ApiResponse.error(400, str(error))
    except Exception as error:
        return ApiResponse.error(500, str(error))

    audio_url = build_public_asset_url(request, generated_audio.relative_url)
    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_app_audio_play(
        audio_url=audio_url,
        message_text=message_text,
        audio_content_type=generated_audio.content_type,
    )
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "message": message_text,
        "filename": generated_audio.filename,
        "audioUrl": audio_url,
        "voiceName": generated_audio.voice_name,
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "online tts audio notification sent"
        if delivered_count > 0
        else "audio generated but no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/ws/harmony/play-library-audio", response_model=ApiResponse)
async def play_library_audio(
    payload: LibraryAudioPlayRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.xfyun_online_tts_service.resolve_library_audio_asset(payload.filename)
    except ValueError as error:
        return ApiResponse.error(400, str(error))
    except FileNotFoundError:
        return ApiResponse.error(404, "audio file not found")

    audio_url = build_public_asset_url(request, library_audio.relative_url)
    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_app_audio_play(
        audio_url=audio_url,
        message_text=library_audio.display_name,
        audio_content_type=library_audio.content_type,
    )
    data = {
        "connectedClients": connected_clients,
        "deliveredCount": delivered_count,
        "filename": library_audio.filename,
        "displayName": library_audio.display_name,
        "audioUrl": audio_url,
        "webSocketPath": "/ws/harmony-app",
    }
    message = (
        "library audio notification sent"
        if delivered_count > 0
        else "audio selected but no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.get("/api/ai/mode", response_model=ApiResponse)
async def get_ai_mode(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.ai_mode_service.build_mode_payload())


@router.post("/api/ai/mode", response_model=ApiResponse)
async def update_ai_mode(
    mode: str = Query(..., description="mode code: mode1/mode2/mode3"),
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


def build_public_asset_url(request: Request, relative_url: str) -> str:
    configured_base_url = settings.public_base_url.strip()
    if configured_base_url != "":
        return f"{configured_base_url.rstrip('/')}{relative_url}"
    return f"{str(request.base_url).rstrip('/')}{relative_url}"
