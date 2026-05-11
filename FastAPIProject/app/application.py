from __future__ import annotations

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.container import AppContainer
from app.controllers.http import router as http_router
from app.controllers.websocket import router as websocket_router
from app.core.config import settings


def create_app() -> FastAPI:
    container = AppContainer()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        os.makedirs(settings.data_dir, exist_ok=True)
        os.makedirs(settings.bt_cache_dir, exist_ok=True)
        os.makedirs(settings.bt_library_dir, exist_ok=True)
        os.makedirs(settings.cp_cache_dir, exist_ok=True)
        os.makedirs(settings.cp_library_dir, exist_ok=True)
        os.makedirs(settings.ai_cache_dir, exist_ok=True)
        os.makedirs(settings.ai_library_dir, exist_ok=True)
        app.state.container = container
        yield

    application = FastAPI(title=settings.app_name, lifespan=lifespan)
    application.mount("/bt_cache", StaticFiles(directory=settings.bt_cache_dir), name="bt_cache")
    application.mount("/bt_library", StaticFiles(directory=settings.bt_library_dir), name="bt_library")
    application.mount("/cp_cache", StaticFiles(directory=settings.cp_cache_dir), name="cp_cache")
    application.mount("/cp_library", StaticFiles(directory=settings.cp_library_dir), name="cp_library")
    application.mount("/ai_cache", StaticFiles(directory=settings.ai_cache_dir), name="ai_cache")
    application.mount("/ai_library", StaticFiles(directory=settings.ai_library_dir), name="ai_library")
    application.include_router(http_router)
    application.include_router(websocket_router)
    return application


app = create_app()


def run() -> None:
    uvicorn.run(app, host=settings.host, port=settings.port, ws="websockets")
