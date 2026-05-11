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
    bt_cache_dir: str = os.getenv(
        "HFOOD_BT_AUDIO_CACHE_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "bt_cache",
        ),
    )
    bt_library_dir: str = os.getenv(
        "HFOOD_BT_AUDIO_LIBRARY_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "bt_library",
        ),
    )
    cp_cache_dir: str = os.getenv(
        "HFOOD_CP_AUDIO_CACHE_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "cp_cache",
        ),
    )
    cp_library_dir: str = os.getenv(
        "HFOOD_CP_AUDIO_LIBRARY_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "cp_library",
        ),
    )
    ai_cache_dir: str = os.getenv(
        "HFOOD_AI_AUDIO_CACHE_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "ai_cache",
        ),
    )
    ai_library_dir: str = os.getenv(
        "HFOOD_AI_AUDIO_LIBRARY_DIR",
        os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
            "ai_library",
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
