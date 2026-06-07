from __future__ import annotations

import asyncio
import ipaddress
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from urllib.parse import quote


if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

logger = logging.getLogger("vrm_render_gateway")
logger.setLevel(logging.INFO)


HOST = os.getenv("VRM_RENDER_HOST", "0.0.0.0")
PORT = int(os.getenv("VRM_RENDER_PORT", "6688"))
PUBLIC_HOST = os.getenv("VRM_RENDER_PUBLIC_HOST", "192.168.110.253")
SESSION_DEFAULT = "default"
OPENLIVE3D_ROOT = os.getenv(
    "OPENLIVE3D_ROOT",
    r"E:\OneLive3D\OpenLive3D.github.io",
)
XRANIMATOR_ROOT = os.getenv(
    "XRANIMATOR_ROOT",
    r"E:\XRANDSYS\SystemAnimatorOnline",
)
RENDERER_HTML = os.getenv(
    "VRM_RENDERER_HTML",
    os.path.join(XRANIMATOR_ROOT, "xr-remote-renderer.html"),
)
XR_REMOTE_APP_HTML = os.path.join(XRANIMATOR_ROOT, "xr-remote-app.html")
XR_REMOTE_VERSION_FILES = [
    XR_REMOTE_APP_HTML,
    os.path.join(XRANIMATOR_ROOT, "xr-remote-renderer.js"),
    os.path.join(XRANIMATOR_ROOT, "images", "XR Animator", "animate.js"),
    os.path.join(XRANIMATOR_ROOT, "MMD.js", "MMD_SA.js"),
    os.path.join(XRANIMATOR_ROOT, "jThree", "index.js"),
    os.path.join(XRANIMATOR_ROOT, "jThree", "script", "v2.1.2_jThree.js"),
    os.path.join(XRANIMATOR_ROOT, "jThree", "plugin", "jThree.XFile.js"),
]
VRM_MODEL_PATH = "/vrm-render/assets/three-vrm-girl.vrm"
VRM_MODEL_FILE = os.path.join(OPENLIVE3D_ROOT, "asset", "vrm", "three-vrm-girl.vrm")


@dataclass
class VrmRenderSession:
    signaling: dict[str, WebSocket] = field(default_factory=dict)
    pose: dict[str, WebSocket] = field(default_factory=dict)
    latest_camera_meta: dict[str, Any] | None = None
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class VrmRenderHub:
    def __init__(self) -> None:
        self._sessions: dict[str, VrmRenderSession] = {}

    def _get_session(self, session_id: str) -> VrmRenderSession:
        normalized = session_id.strip() or SESSION_DEFAULT
        if normalized not in self._sessions:
            self._sessions[normalized] = VrmRenderSession()
        return self._sessions[normalized]

    async def connect(self, channel: str, session_id: str, role: str, websocket: WebSocket) -> bool:
        await websocket.accept()
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        previous_socket: WebSocket | None = None
        rejected = False
        sockets_to_close: list[WebSocket] = []
        existing_renderer_sockets: list[WebSocket] = []
        async with session.lock:
            old = peers.get(role)
            if role == "renderer":
                existing_renderer_sockets = self._collect_renderer_sockets(session, exclude=websocket)
                if self._should_reject_renderer(session_id, session, websocket):
                    rejected = True
                else:
                    peers[role] = websocket
                    sockets_to_close = [
                        candidate for candidate in existing_renderer_sockets
                        if (
                            candidate is not websocket
                            and candidate is not peers[role]
                            and not self._is_same_renderer_owner(candidate, websocket)
                        )
                    ]
            else:
                if old is not None and old is not websocket:
                    previous_socket = old
                peers[role] = websocket
        if rejected:
            existing_clients = [getattr(item, "client", None) for item in existing_renderer_sockets]
            logger.info(
                "ws reject channel=%s session=%s role=%s existing_clients=%s new_client=%s reason=%s",
                channel,
                session_id,
                role,
                existing_clients,
                getattr(websocket, "client", None),
                "loopback renderer is blocked for this session",
            )
            await self._send_json(websocket, {
                "type": "connection_rejected",
                "channel": channel,
                "sessionId": session_id,
                "role": role,
                "reason": "loopback renderer blocked for session",
            })
            await self._close_silently(websocket, 1013, "loopback renderer blocked for session")
            return False
        for socket_to_close in sockets_to_close:
            logger.info(
                "ws renderer-owner-replace session=%s new_client=%s old_client=%s",
                session_id,
                getattr(websocket, "client", None),
                getattr(socket_to_close, "client", None),
            )
            await self._close_silently(socket_to_close, 1012, "replaced by newer connection")
        if previous_socket is not None:
            logger.info(
                "ws replace channel=%s session=%s role=%s old_client=%s new_client=%s",
                channel,
                session_id,
                role,
                getattr(previous_socket, "client", None),
                getattr(websocket, "client", None),
            )
            await self._close_silently(previous_socket, 1012, "replaced by newer connection")
        logger.info(
            "ws connect channel=%s session=%s role=%s peer_connected=%s client=%s",
            channel,
            session_id,
            role,
            self._peer_role(role) in peers,
            getattr(websocket, "client", None),
        )
        await self._send_json(websocket, {
            "type": "connected",
            "channel": channel,
            "sessionId": session_id,
            "role": role,
            "peerConnected": self._peer_role(role) in peers,
        })
        if channel == "pose" and role == "renderer" and session.latest_camera_meta is not None:
            await self._send_json(websocket, session.latest_camera_meta)
        await self._notify_peer_state(channel, session_id)
        return True

    async def disconnect(self, channel: str, session_id: str, role: str, websocket: WebSocket) -> None:
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        async with session.lock:
            if peers.get(role) is websocket:
                del peers[role]
        logger.info(
            "ws disconnect channel=%s session=%s role=%s client=%s",
            channel,
            session_id,
            role,
            getattr(websocket, "client", None),
        )
        await self._notify_peer_state(channel, session_id)

    async def relay(self, channel: str, session_id: str, role: str, payload: Any) -> None:
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        target_role = self._read_target_role(payload) or self._peer_role(role)
        target = peers.get(target_role)
        payload_type = self._read_payload_type(payload)
        if channel == "pose" and role == "tablet" and payload_type == "camera_meta" and isinstance(payload, dict):
            session.latest_camera_meta = dict(payload)
        if target is None:
            if channel == "pose" and payload_type == "camera_meta":
                logger.info(
                    "ws relay deferred channel=%s session=%s from=%s to=%s type=%s",
                    channel,
                    session_id,
                    role,
                    target_role,
                    payload_type,
                )
                return
            logger.warning(
                "ws relay miss channel=%s session=%s from=%s to=%s type=%s",
                channel,
                session_id,
                role,
                target_role,
                payload_type,
            )
            source = peers.get(role)
            if source is not None:
                await self._send_json(source, {
                    "type": "peer_unavailable",
                    "channel": channel,
                    "sessionId": session_id,
                    "target": target_role,
                })
            return
        logger.info(
            "ws relay channel=%s session=%s from=%s to=%s type=%s",
            channel,
            session_id,
            role,
            target_role,
            payload_type,
        )
        await self._send_json(target, payload)

    async def _notify_peer_state(self, channel: str, session_id: str) -> None:
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        for role, websocket in list(peers.items()):
            await self._send_json(websocket, {
                "type": "peer_state",
                "channel": channel,
                "sessionId": session_id,
                "role": role,
                "peerConnected": self._peer_role(role) in peers,
            })

    @staticmethod
    def _peer_role(role: str) -> str:
        return "renderer" if role == "tablet" else "tablet"

    @classmethod
    def _should_reject_replacement(cls, role: str, old: WebSocket, new: WebSocket) -> bool:
        if role != "renderer":
            return False
        return cls._is_loopback_client(new) and not cls._is_loopback_client(old)

    @classmethod
    def _should_reject_renderer(cls, session_id: str, session: VrmRenderSession, new: WebSocket) -> bool:
        new_is_loopback = cls._is_loopback_client(new)
        if session_id == SESSION_DEFAULT and new_is_loopback:
            return True
        if not new_is_loopback:
            return False
        for candidate in cls._collect_renderer_sockets(session, exclude=new):
            if not cls._is_loopback_client(candidate):
                return True
        return False

    @staticmethod
    def _collect_renderer_sockets(session: VrmRenderSession, exclude: WebSocket | None = None) -> list[WebSocket]:
        sockets: list[WebSocket] = []
        for peers in (session.signaling, session.pose):
            websocket = peers.get("renderer")
            if websocket is None or websocket is exclude:
                continue
            if websocket not in sockets:
                sockets.append(websocket)
        return sockets

    @staticmethod
    def _is_same_renderer_owner(left: WebSocket, right: WebSocket) -> bool:
        left_client = getattr(left, "client", None)
        right_client = getattr(right, "client", None)
        left_host = getattr(left_client, "host", "") if left_client is not None else ""
        right_host = getattr(right_client, "host", "") if right_client is not None else ""
        if not left_host or not right_host:
            return False
        return left_host == right_host

    @staticmethod
    def _is_loopback_client(websocket: WebSocket) -> bool:
        client = getattr(websocket, "client", None)
        host = getattr(client, "host", "") if client is not None else ""
        if not host:
            return False
        normalized = host.strip().lower()
        if normalized == "localhost":
            return True
        try:
            return ipaddress.ip_address(normalized).is_loopback
        except ValueError:
            return False

    @staticmethod
    def _read_target_role(payload: Any) -> str:
        if isinstance(payload, dict):
            value = payload.get("to")
            if value == "tablet" or value == "renderer":
                return value
        return ""

    @staticmethod
    def _read_payload_type(payload: Any) -> str:
        if isinstance(payload, dict):
            value = payload.get("type")
            if isinstance(value, str) and value:
                return value
        return "unknown"

    @staticmethod
    async def _send_json(websocket: WebSocket, payload: Any) -> None:
        try:
            await websocket.send_text(json.dumps(payload, ensure_ascii=False))
        except Exception:
            pass

    @staticmethod
    async def _close_silently(websocket: WebSocket, code: int, reason: str) -> None:
        try:
            await websocket.close(code=code, reason=reason)
        except Exception:
            pass


hub = VrmRenderHub()
app = FastAPI(title="Hfood VRM Render Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.isdir(OPENLIVE3D_ROOT):
    app.mount("/openlive3d", StaticFiles(directory=OPENLIVE3D_ROOT), name="openlive3d")
if os.path.isdir(XRANIMATOR_ROOT):
    app.mount("/xranimator", StaticFiles(directory=XRANIMATOR_ROOT), name="xranimator")


def build_no_cache_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }


def build_renderer_iframe_src(session_id: str, model_url: str) -> str:
    cache_buster = build_xr_asset_version()
    return (
        "/xranimator/xr-remote-app.html"
        f"?sessionId={quote(session_id)}"
        f"&model={quote(model_url, safe=':/?&=%')}"
        f"&v={quote(cache_buster)}"
    )


def build_xr_asset_version() -> str:
    latest_mtime = 0
    for path in XR_REMOTE_VERSION_FILES:
        try:
            latest_mtime = max(latest_mtime, int(os.path.getmtime(path)))
        except OSError:
            continue
    return str(latest_mtime or 0)


def build_renderer_html(session_id: str, model_url: str) -> str:
    iframe_src = build_renderer_iframe_src(session_id, model_url)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hfood XR Core Remote Renderer</title>
    <style>
      html,
      body {{
        margin: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #eef3f7;
        font-family: "Microsoft YaHei", sans-serif;
      }}

      #xraFrame,
      #relayCanvas {{
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        border: 0;
      }}

      #relayCanvas {{
        pointer-events: none;
        opacity: 0;
      }}

      #status {{
        position: fixed;
        left: 16px;
        top: 16px;
        z-index: 20;
        max-width: 620px;
        padding: 10px 12px;
        border-radius: 12px;
        border: 1px solid rgba(15, 23, 42, 0.12);
        background: rgba(255, 255, 255, 0.72);
        color: #0f172a;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.14);
        backdrop-filter: blur(12px);
        font-size: 12px;
        line-height: 1.55;
      }}

      #title {{
        font-weight: 800;
      }}

      #message {{
        margin-top: 4px;
        color: #475569;
      }}
    </style>
  </head>
  <body>
    <iframe id="xraFrame" src="{iframe_src}"></iframe>
    <canvas id="relayCanvas" width="1920" height="1080"></canvas>
    <div id="status">
      <div id="title">XR core renderer starting</div>
      <div id="message">Waiting for tablet camera uplink so the PC can drive full-body rendering.</div>
    </div>
    <script src="/xranimator/xr-remote-renderer.js"></script>
  </body>
</html>
"""


@app.get("/vrm-render/config")
async def get_vrm_render_config() -> JSONResponse:
    base_http = f"http://{PUBLIC_HOST}:{PORT}"
    base_ws = f"ws://{PUBLIC_HOST}:{PORT}"
    return JSONResponse({
        "sessionId": SESSION_DEFAULT,
        "rendererUrl": f"{base_http}/vrm-renderer?sessionId={SESSION_DEFAULT}",
        "signalingUrl": f"{base_ws}/ws/vrm-render/signaling/{SESSION_DEFAULT}/tablet",
        "poseUrl": f"{base_ws}/ws/vrm-render/pose/{SESSION_DEFAULT}/tablet",
        "rendererSignalingUrl": f"{base_ws}/ws/vrm-render/signaling/{SESSION_DEFAULT}/renderer",
        "rendererPoseUrl": f"{base_ws}/ws/vrm-render/pose/{SESSION_DEFAULT}/renderer",
        "modelUrl": f"{base_http}{VRM_MODEL_PATH}",
        "rendererEngine": "xr-core-drive",
    }, headers=build_no_cache_headers())


@app.get("/vrm-render/assets/three-vrm-girl.vrm")
async def get_builtin_vrm_model() -> FileResponse:
    if not os.path.isfile(VRM_MODEL_FILE):
        raise HTTPException(status_code=404, detail=f"VRM model not found: {VRM_MODEL_FILE}")
    response = FileResponse(
        VRM_MODEL_FILE,
        media_type="model/gltf-binary",
        filename="three-vrm-girl.vrm",
    )
    for key, value in build_no_cache_headers().items():
        response.headers[key] = value
    response.headers["Content-Type"] = "model/gltf-binary"
    return response


@app.get("/vrm-renderer")
async def get_vrm_renderer(sessionId: str = SESSION_DEFAULT, model: str | None = None) -> HTMLResponse:
    normalized_session_id = sessionId.strip() or SESSION_DEFAULT
    base_http = f"http://{PUBLIC_HOST}:{PORT}"
    model_url = model.strip() if isinstance(model, str) and model.strip() else f"{base_http}{VRM_MODEL_PATH}"
    return HTMLResponse(
        build_renderer_html(normalized_session_id, model_url),
        headers=build_no_cache_headers(),
    )


@app.get("/xranimator/xr-remote-app.html")
async def get_xr_remote_app() -> FileResponse:
    if not os.path.isfile(XR_REMOTE_APP_HTML):
        raise HTTPException(status_code=404, detail=f"XR remote app page not found: {XR_REMOTE_APP_HTML}")
    response = FileResponse(XR_REMOTE_APP_HTML)
    for key, value in build_no_cache_headers().items():
      response.headers[key] = value
    return response


async def websocket_loop(channel: str, session_id: str, role: str, websocket: WebSocket) -> None:
    connected = await hub.connect(channel, session_id, role, websocket)
    if not connected:
        return
    try:
        while True:
            text = await websocket.receive_text()
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                payload = {"type": "text", "payload": text}
            if isinstance(payload, dict):
                payload.setdefault("sessionId", session_id)
                payload.setdefault("from", role)
            await hub.relay(channel, session_id, role, payload)
    except WebSocketDisconnect as exc:
        logger.info(
            "ws disconnect event channel=%s session=%s role=%s code=%s client=%s",
            channel,
            session_id,
            role,
            getattr(exc, "code", None),
            getattr(websocket, "client", None),
        )
    except RuntimeError as exc:
        message = str(exc)
        if 'WebSocket is not connected. Need to call "accept" first.' in message:
            logger.info(
                "ws runtime-close channel=%s session=%s role=%s client=%s detail=%s",
                channel,
                session_id,
                role,
                getattr(websocket, "client", None),
                message,
            )
        else:
            raise
    finally:
        await hub.disconnect(channel, session_id, role, websocket)


@app.websocket("/ws/vrm-render/signaling/{session_id}/{role}")
async def signaling_socket(websocket: WebSocket, session_id: str, role: str) -> None:
    await websocket_loop("signaling", session_id, role, websocket)


@app.websocket("/ws/vrm-render/pose/{session_id}/{role}")
async def pose_socket(websocket: WebSocket, session_id: str, role: str) -> None:
    await websocket_loop("pose", session_id, role, websocket)


def run() -> None:
    uvicorn.run(app, host=HOST, port=PORT, ws="websockets")


if __name__ == "__main__":
    run()
