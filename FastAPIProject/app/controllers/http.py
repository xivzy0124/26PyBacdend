from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.container import AppContainer, get_container_from_request
from app.core.config import settings
from app.models.schemas import (
    ApiResponse,
    BubbleMessageRequest,
    LibraryAudioPlayRequest,
    LibraryAudioPromoteRequest,
    OnlineTtsRequest,
    PostureDemoCommandRequest,
)
from app.views.ws_control_page import render_ws_control_page

router = APIRouter()


POSTURE_DEMO_PRESETS: dict[str, dict[str, object]] = {
    "render": {
        "mode": "render",
        "title": "渲染",
        "message": "右侧加载模型3并保持默认动作，不进行人体识别和驱动",
        "phase": "ready",
        "bodyDetected": False,
        "trackingReady": False,
        "cameraActive": False,
        "demoLocked": False,
    },
    "stage2": {
        "mode": "stage2",
        "title": "阶段二",
        "message": "右侧模型3进入数字孪生驱动，但保留明显抖动问题",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "demoLocked": False,
    },
    "stage3": {
        "mode": "stage3",
        "title": "阶段三",
        "message": "右侧模型3继续数字孪生驱动，但存在高延迟",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "demoLocked": False,
    },
    "stage4": {
        "mode": "stage4",
        "title": "阶段四",
        "message": "右侧模型3恢复正常数字孪生实时驱动",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "demoLocked": False,
    },
    "normal": {
        "mode": "normal",
        "title": "默认",
        "message": "退出演示态并回到空白准备状态",
        "phase": "ready",
        "bodyDetected": False,
        "trackingReady": False,
        "cameraActive": False,
        "demoLocked": False,
    },
}

DEMO_POSTURE_PRESETS: dict[str, dict[str, object]] = {
    "render": {
        "mode": "render",
        "title": "渲染",
        "message": "右侧显示渲染中进度条，60秒后展示 sr.glb 静态默认姿态",
        "phase": "ready",
        "bodyDetected": False,
        "trackingReady": False,
        "cameraActive": False,
        "autoNavigate": True,
    },
    "stage2": {
        "mode": "stage2",
        "title": "跳变",
        "message": "sr.glb 进入明显跳变与抖动驱动演示",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "autoNavigate": True,
    },
    "stage3": {
        "mode": "stage3",
        "title": "延迟",
        "message": "sr.glb 进入高延迟驱动演示",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "autoNavigate": True,
    },
    "stage4": {
        "mode": "stage4",
        "title": "正常",
        "message": "sr.glb 恢复完全正常的实时驱动",
        "phase": "tracking",
        "bodyDetected": True,
        "trackingReady": True,
        "cameraActive": True,
        "autoNavigate": True,
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


@router.post("/api/ws/harmony/demo-posture", response_model=ApiResponse)
async def notify_demo_posture(
    payload: PostureDemoCommandRequest,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    action = payload.action.strip().lower()
    demo_preset = DEMO_POSTURE_PRESETS.get(action)
    if demo_preset is None:
        return ApiResponse.error(400, f"unsupported demo posture action: {payload.action}")

    connected_clients = container.connection_manager.get_connected_count()
    delivered_count = await container.connection_manager.send_demo_posture_command(
        mode=str(demo_preset["mode"]),
        title=str(demo_preset["title"]),
        message_text=str(demo_preset["message"]),
        phase=str(demo_preset["phase"]),
        body_detected=bool(demo_preset["bodyDetected"]),
        tracking_ready=bool(demo_preset["trackingReady"]),
        camera_active=bool(demo_preset["cameraActive"]),
        auto_navigate=bool(demo_preset["autoNavigate"]),
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
        "demo posture command sent"
        if delivered_count > 0
        else "no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.get("/api/tts/bt/config", response_model=ApiResponse)
async def get_bt_online_tts_config(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.bt_online_tts_service.build_runtime_payload())


@router.get("/api/tts/bt/library", response_model=ApiResponse)
async def get_bt_online_tts_library(
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    library_assets = container.bt_online_tts_service.list_library_audio_assets()
    data = [
        {
            "filename": asset.filename,
            "displayName": asset.display_name,
            "audioUrl": build_public_asset_url(request, asset.relative_url),
        }
        for asset in library_assets
    ]
    return ApiResponse.success(data)


@router.post("/api/ws/harmony/notify-bt-online-tts", response_model=ApiResponse)
async def notify_bt_online_tts(
    payload: OnlineTtsRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    message_text = payload.message.strip()
    if message_text == "":
        return ApiResponse.error(400, "message cannot be empty")

    try:
        generated_audio = await container.bt_online_tts_service.synthesize_to_cache(
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


@router.post("/api/ws/harmony/play-bt-library-audio", response_model=ApiResponse)
async def play_bt_library_audio(
    payload: LibraryAudioPlayRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.bt_online_tts_service.resolve_library_audio_asset(payload.filename)
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


@router.post("/api/tts/bt/promote-cache", response_model=ApiResponse)
async def promote_bt_cache_audio(
    payload: LibraryAudioPromoteRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.bt_online_tts_service.promote_cache_audio_to_library(payload.filename)
    except ValueError as error:
        return ApiResponse.error(400, str(error))
    except FileNotFoundError:
        return ApiResponse.error(404, "cache audio file not found")

    return ApiResponse.success({
        "filename": library_audio.filename,
        "displayName": library_audio.display_name,
        "audioUrl": build_public_asset_url(request, library_audio.relative_url),
    }, "bt cache audio promoted to library")


@router.get("/api/tts/cp/config", response_model=ApiResponse)
async def get_cp_online_tts_config(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.cp_online_tts_service.build_runtime_payload())


@router.get("/api/tts/cp/library", response_model=ApiResponse)
async def get_cp_online_tts_library(
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    library_assets = container.cp_online_tts_service.list_library_audio_assets()
    data = [
        {
            "filename": asset.filename,
            "displayName": asset.display_name,
            "audioUrl": build_public_asset_url(request, asset.relative_url),
        }
        for asset in library_assets
    ]
    return ApiResponse.success(data)


@router.post("/api/ws/harmony/notify-cp-online-tts", response_model=ApiResponse)
async def notify_cp_online_tts(
    payload: OnlineTtsRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    message_text = payload.message.strip()
    if message_text == "":
        return ApiResponse.error(400, "message cannot be empty")

    try:
        generated_audio = await container.cp_online_tts_service.synthesize_to_cache(
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
        "cv online tts audio notification sent"
        if delivered_count > 0
        else "audio generated but no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/ws/harmony/play-cp-library-audio", response_model=ApiResponse)
async def play_cp_library_audio(
    payload: LibraryAudioPlayRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.cp_online_tts_service.resolve_library_audio_asset(payload.filename)
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
        "cv library audio notification sent"
        if delivered_count > 0
        else "audio selected but no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/tts/cp/promote-cache", response_model=ApiResponse)
async def promote_cp_cache_audio(
    payload: LibraryAudioPromoteRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.cp_online_tts_service.promote_cache_audio_to_library(payload.filename)
    except ValueError as error:
        return ApiResponse.error(400, str(error))
    except FileNotFoundError:
        return ApiResponse.error(404, "cache audio file not found")

    return ApiResponse.success({
        "filename": library_audio.filename,
        "displayName": library_audio.display_name,
        "audioUrl": build_public_asset_url(request, library_audio.relative_url),
    }, "cp cache audio promoted to library")


@router.get("/api/tts/ai/config", response_model=ApiResponse)
async def get_ai_online_tts_config(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.ai_online_tts_service.build_runtime_payload())


@router.get("/api/tts/ai/library", response_model=ApiResponse)
async def get_ai_online_tts_library(
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    library_assets = container.ai_online_tts_service.list_library_audio_assets()
    data = [
        {
            "filename": asset.filename,
            "displayName": asset.display_name,
            "audioUrl": build_public_asset_url(request, asset.relative_url),
        }
        for asset in library_assets
    ]
    return ApiResponse.success(data)


@router.post("/api/ws/harmony/notify-ai-online-tts", response_model=ApiResponse)
async def notify_ai_online_tts(
    payload: OnlineTtsRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    message_text = payload.message.strip()
    if message_text == "":
        return ApiResponse.error(400, "message cannot be empty")

    try:
        generated_audio = await container.ai_online_tts_service.synthesize_to_cache(
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
        "ai online tts audio notification sent"
        if delivered_count > 0
        else "audio generated but no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/ws/harmony/play-ai-library-audio", response_model=ApiResponse)
async def play_ai_library_audio(
    payload: LibraryAudioPlayRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.ai_online_tts_service.resolve_library_audio_asset(payload.filename)
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
        "ai library audio notification sent"
        if delivered_count > 0
        else "audio selected but no Harmony app websocket clients connected"
    )
    return ApiResponse.success(data, message)


@router.post("/api/tts/ai/promote-cache", response_model=ApiResponse)
async def promote_ai_cache_audio(
    payload: LibraryAudioPromoteRequest,
    request: Request,
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        library_audio = container.ai_online_tts_service.promote_cache_audio_to_library(payload.filename)
    except ValueError as error:
        return ApiResponse.error(400, str(error))
    except FileNotFoundError:
        return ApiResponse.error(404, "cache audio file not found")

    return ApiResponse.success({
        "filename": library_audio.filename,
        "displayName": library_audio.display_name,
        "audioUrl": build_public_asset_url(request, library_audio.relative_url),
    }, "ai cache audio promoted to library")


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


@router.get("/api/pressure/demo-mode", response_model=ApiResponse)
async def get_pressure_demo_mode(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.pressure_demo_mode_service.build_mode_payload())


@router.post("/api/pressure/demo-mode", response_model=ApiResponse)
async def update_pressure_demo_mode(
    mode: str = Query(..., description="pressure demo mode: empty/direct/repair"),
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        container.pressure_demo_mode_service.update_mode(mode)
        mode_payload = container.pressure_demo_mode_service.build_mode_payload()
        broadcast_message = container.pressure_demo_mode_service.build_mode_changed_message()
        await container.connection_manager.broadcast(broadcast_message)
        return ApiResponse.success(mode_payload, broadcast_message.message)
    except ValueError as error:
        return ApiResponse.error(400, str(error))


@router.get("/api/pressure/trace-mode", response_model=ApiResponse)
async def get_pressure_trace_demo_mode(
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    return ApiResponse.success(container.pressure_trace_demo_mode_service.build_mode_payload())


@router.post("/api/pressure/trace-mode", response_model=ApiResponse)
async def update_pressure_trace_demo_mode(
    mode: str = Query(..., description="pressure trace demo mode: normal/jitter"),
    container: AppContainer = Depends(get_container_from_request),
) -> ApiResponse:
    try:
        container.pressure_trace_demo_mode_service.update_mode(mode)
        mode_payload = container.pressure_trace_demo_mode_service.build_mode_payload()
        broadcast_message = container.pressure_trace_demo_mode_service.build_mode_changed_message()
        await container.connection_manager.broadcast(broadcast_message)
        return ApiResponse.success(mode_payload, broadcast_message.message)
    except ValueError as error:
        return ApiResponse.error(400, str(error))


def build_public_asset_url(request: Request, relative_url: str) -> str:
    configured_base_url = settings.public_base_url.strip()
    if configured_base_url != "":
        return f"{configured_base_url.rstrip('/')}{relative_url}"
    return f"{str(request.base_url).rstrip('/')}{relative_url}"

