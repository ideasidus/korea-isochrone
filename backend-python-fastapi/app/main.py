from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.isochrone import router as isochrone_router
from app.clients.otp_client import OtpClient
from app.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        timeout = httpx.Timeout(settings.request_timeout_seconds)
        async with httpx.AsyncClient(
            base_url=str(settings.otp_base_url),
            timeout=timeout,
        ) as http_client:
            app.state.otp_client = OtpClient(
                http_client=http_client,
                router_id=settings.otp_router_id,
                retries=settings.request_retries,
                backoff_seconds=settings.request_backoff_seconds,
            )
            yield

    application = FastAPI(
        title="Korea Isochrone API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(isochrone_router)
    return application


app = create_app()

