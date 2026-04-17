from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(slots=True)
class AppSettings:
    app_name: str = "Hfood Harmony Backend"
    host: str = os.getenv("HFOOD_HOST", "0.0.0.0")
    # Keep the backend port aligned with the Harmony app ApiConfig.
    port: int = 8080


settings = AppSettings()
