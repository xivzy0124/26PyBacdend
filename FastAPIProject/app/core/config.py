from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(slots=True)
class AppSettings:
    app_name: str = "Hfood Harmony Backend"
    host: str = os.getenv("HFOOD_HOST", "0.0.0.0")
    # Keep the backend port aligned with the Harmony app ApiConfig.
    port: int = 8080
    audio_cache_max_files: int = int(os.getenv("HFOOD_AUDIO_CACHE_MAX_FILES", "40"))
    public_base_url: str = os.getenv("HFOOD_PUBLIC_BASE_URL", "").strip()
    data_dir: str = os.getenv(
        "HFOOD_DATA_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
    )
    audio_cache_dir: str = os.getenv(
        "HFOOD_AUDIO_CACHE_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "audio_cache",
        ),
    )
    audio_library_dir: str = os.getenv(
        "HFOOD_AUDIO_LIBRARY_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "audio_library",
        ),
    )
    xfyun_account_store_path: str = os.getenv(
        "HFOOD_XFYUN_ACCOUNT_STORE_PATH",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "xfyun_tts_accounts.json",
        ),
    )


settings = AppSettings()
