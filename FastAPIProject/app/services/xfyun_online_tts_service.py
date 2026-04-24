from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
import hashlib
import hmac
import json
import os
from threading import RLock
from urllib.parse import urlencode
from uuid import uuid4

from websockets.asyncio.client import connect

from app.core.config import settings
from app.services.xfyun_tts_account_service import XfyunTtsAccountService

XFYUN_TTS_HOST = "tts-api.xfyun.cn"
XFYUN_TTS_PATH = "/v2/tts"
XFYUN_TTS_URL = f"wss://{XFYUN_TTS_HOST}{XFYUN_TTS_PATH}"

DEFAULT_VOICE_OPTIONS: list[dict[str, str]] = [
    {"label": "小燕", "value": "xiaoyan"},
    {"label": "小宇", "value": "xiaoyu"},
    {"label": "小美", "value": "xiaomei"},
    {"label": "小峰", "value": "xiaofeng"},
    {"label": "小萍", "value": "xiaoping"},
    {"label": "许久", "value": "x_john"},
]


@dataclass(slots=True)
class GeneratedAudioAsset:
    filename: str
    relative_url: str
    content_type: str
    voice_name: str
    message_text: str


class XfyunOnlineTtsService:
    def __init__(
        self,
        account_service: XfyunTtsAccountService,
        audio_cache_dir: str | None = None,
    ) -> None:
        self._account_service = account_service
        self._audio_cache_dir = audio_cache_dir or settings.audio_cache_dir
        self._audio_cache_max_files = max(1, settings.audio_cache_max_files)
        self._lock = RLock()
        os.makedirs(self._audio_cache_dir, exist_ok=True)

    def get_audio_cache_dir(self) -> str:
        return self._audio_cache_dir

    def build_runtime_payload(self) -> dict:
        active_account = self._account_service.get_active_account()
        return {
            "activeAccountName": active_account.name if active_account is not None else None,
            "activeAccountId": active_account.accountId if active_account is not None else None,
            "defaultVcn": active_account.defaultVcn if active_account is not None else "xiaoyan",
            "voiceOptions": DEFAULT_VOICE_OPTIONS,
        }

    async def synthesize_to_cache(
        self,
        message_text: str,
        vcn: str | None = None,
    ) -> GeneratedAudioAsset:
        normalized_text = message_text.strip()
        if normalized_text == "":
            raise ValueError("message cannot be empty")

        active_account = self._account_service.get_active_account()
        if active_account is None:
            raise ValueError("no active XFYun TTS account configured")
        if not active_account.enabled:
            raise ValueError("active XFYun TTS account is disabled")

        target_vcn = (vcn or active_account.defaultVcn or "xiaoyan").strip() or "xiaoyan"
        auth_query = self._build_auth_query(
            api_key=active_account.apiKey,
            api_secret=active_account.apiSecret,
        )
        audio_bytes = await self._fetch_audio_bytes(
            url=f"{XFYUN_TTS_URL}?{auth_query}",
            app_id=active_account.appId,
            text=normalized_text,
            vcn=target_vcn,
        )
        filename = self._build_audio_filename(target_vcn)
        file_path = os.path.join(self._audio_cache_dir, filename)
        with self._lock:
            with open(file_path, "wb") as file:
                file.write(audio_bytes)
            self._cleanup_audio_cache_locked()

        return GeneratedAudioAsset(
            filename=filename,
            relative_url=f"/audio-cache/{filename}",
            content_type="audio/mpeg",
            voice_name=target_vcn,
            message_text=normalized_text,
        )

    def _build_auth_query(self, api_key: str, api_secret: str) -> str:
        date_value = format_datetime(datetime.now(timezone.utc), usegmt=True)
        signature_origin = (
            f"host: {XFYUN_TTS_HOST}\n"
            f"date: {date_value}\n"
            f"GET {XFYUN_TTS_PATH} HTTP/1.1"
        )
        signature = base64.b64encode(
            hmac.new(
                api_secret.encode("utf-8"),
                signature_origin.encode("utf-8"),
                digestmod=hashlib.sha256,
            ).digest()
        ).decode("utf-8")
        authorization_origin = (
            f'api_key="{api_key}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature}"'
        )
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")
        return urlencode(
            {
                "authorization": authorization,
                "date": date_value,
                "host": XFYUN_TTS_HOST,
            }
        )

    async def _fetch_audio_bytes(
        self,
        url: str,
        app_id: str,
        text: str,
        vcn: str,
    ) -> bytes:
        payload = {
            "common": {
                "app_id": app_id,
            },
            "business": {
                "aue": "lame",
                "auf": "audio/L16;rate=16000",
                "vcn": vcn,
                "tte": "UTF8",
            },
            "data": {
                "status": 2,
                "text": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
            },
        }

        audio_chunks: list[bytes] = []
        async with connect(url, max_size=None) as websocket:
            await websocket.send(json.dumps(payload))
            async for response_text in websocket:
                response = json.loads(response_text)
                code = int(response.get("code", 0))
                if code != 0:
                    message = response.get("message") or response.get("sid") or "unknown_xfyun_error"
                    raise RuntimeError(f"xfyun tts failed: code={code}, message={message}")

                data = response.get("data") or {}
                audio_base64 = str(data.get("audio") or "")
                if audio_base64:
                    audio_chunks.append(base64.b64decode(audio_base64))

                if int(data.get("status", 2)) == 2:
                    break

        audio_bytes = b"".join(audio_chunks)
        if len(audio_bytes) <= 0:
            raise RuntimeError("xfyun tts returned empty audio")
        return audio_bytes

    def _build_audio_filename(self, vcn: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_vcn = "".join(ch for ch in vcn if ch.isalnum() or ch in {"_", "-"}) or "voice"
        return f"{timestamp}_{safe_vcn}_{uuid4().hex[:10]}.mp3"

    def _cleanup_audio_cache_locked(self) -> None:
        cache_entries: list[tuple[float, str]] = []
        with os.scandir(self._audio_cache_dir) as iterator:
            for entry in iterator:
                if not entry.is_file():
                    continue
                if not entry.name.lower().endswith(".mp3"):
                    continue
                try:
                    stat = entry.stat()
                except OSError:
                    continue
                cache_entries.append((stat.st_mtime, entry.path))

        if len(cache_entries) <= self._audio_cache_max_files:
            return

        cache_entries.sort(key=lambda item: item[0], reverse=True)
        for _, stale_path in cache_entries[self._audio_cache_max_files :]:
            try:
                os.remove(stale_path)
            except OSError:
                continue
