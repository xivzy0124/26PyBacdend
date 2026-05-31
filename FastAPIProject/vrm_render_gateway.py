from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


HOST = os.getenv("VRM_RENDER_HOST", "0.0.0.0")
PORT = int(os.getenv("VRM_RENDER_PORT", "6688"))
PUBLIC_HOST = os.getenv("VRM_RENDER_PUBLIC_HOST", "192.168.110.253")
SESSION_DEFAULT = "default"
OPENLIVE3D_ROOT = os.getenv(
    "OPENLIVE3D_ROOT",
    r"E:\OneLive3D\OpenLive3D.github.io",
)
RENDERER_HTML = os.path.join(OPENLIVE3D_ROOT, "vrm-remote-renderer.html")
VRM_MODEL_PATH = "/openlive3d/asset/vrm/three-vrm-girl.vrm"


@dataclass
class VrmRenderSession:
    signaling: dict[str, WebSocket] = field(default_factory=dict)
    pose: dict[str, WebSocket] = field(default_factory=dict)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class VrmRenderHub:
    def __init__(self) -> None:
        self._sessions: dict[str, VrmRenderSession] = {}

    def _get_session(self, session_id: str) -> VrmRenderSession:
        normalized = session_id.strip() or SESSION_DEFAULT
        if normalized not in self._sessions:
            self._sessions[normalized] = VrmRenderSession()
        return self._sessions[normalized]

    async def connect(self, channel: str, session_id: str, role: str, websocket: WebSocket) -> None:
        await websocket.accept()
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        replaced = False
        async with session.lock:
            old = peers.get(role)
            replaced = old is not None and old is not websocket
            peers[role] = websocket
        if replaced:
            # Do not close the old socket here. Some embedded WebViews briefly open
            # duplicate renderer sockets during reload; closing the previous socket
            # can create an open/close storm and make the WebRTC video flicker.
            pass
        await self._send_json(websocket, {
            "type": "connected",
            "channel": channel,
            "sessionId": session_id,
            "role": role,
            "peerConnected": self._peer_role(role) in peers,
        })
        await self._notify_peer_state(channel, session_id)

    async def disconnect(self, channel: str, session_id: str, role: str, websocket: WebSocket) -> None:
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        async with session.lock:
            if peers.get(role) is websocket:
                del peers[role]
        await self._notify_peer_state(channel, session_id)

    async def relay(self, channel: str, session_id: str, role: str, payload: Any) -> None:
        session = self._get_session(session_id)
        peers = session.signaling if channel == "signaling" else session.pose
        target_role = self._read_target_role(payload) or self._peer_role(role)
        target = peers.get(target_role)
        if target is None:
            source = peers.get(role)
            if source is not None:
                await self._send_json(source, {
                    "type": "peer_unavailable",
                    "channel": channel,
                    "sessionId": session_id,
                    "target": target_role,
                })
            return
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

    @staticmethod
    def _read_target_role(payload: Any) -> str:
        if isinstance(payload, dict):
            value = payload.get("to")
            if value == "tablet" or value == "renderer":
                return value
        return ""

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
    })


@app.get("/vrm-renderer")
async def get_vrm_renderer() -> FileResponse:
    if not os.path.isfile(RENDERER_HTML):
        raise HTTPException(status_code=404, detail=f"Renderer page not found: {RENDERER_HTML}")
    return FileResponse(RENDERER_HTML)


async def websocket_loop(channel: str, session_id: str, role: str, websocket: WebSocket) -> None:
    await hub.connect(channel, session_id, role, websocket)
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
    except WebSocketDisconnect:
        pass
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
