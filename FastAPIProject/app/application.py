from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from app.container import AppContainer
from app.controllers.http import router as http_router
from app.controllers.websocket import router as websocket_router
from app.core.config import settings


def create_app() -> FastAPI:
    container = AppContainer()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.container = container
        yield

    application = FastAPI(title=settings.app_name, lifespan=lifespan)
    application.include_router(http_router)
    application.include_router(websocket_router)
    return application


app = create_app()


def run() -> None:
    uvicorn.run(app, host=settings.host, port=settings.port, ws="websockets")
