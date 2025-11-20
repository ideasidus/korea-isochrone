from functools import lru_cache
from typing import Any

from pydantic import AnyHttpUrl, Field, PositiveFloat, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    otp_base_url: AnyHttpUrl = Field(
        "http://otp:8080/otp",
        alias="OTP_API_BASE_URL",
        description="Base URL for the internal OTP service",
    )
    otp_router_id: str = Field(
        "default",
        alias="OTP_ROUTER_ID",
        description="Router ID exposed by OTP (defaults to 'default')",
        min_length=1,
    )
    request_timeout_seconds: PositiveFloat = Field(
        10.0,
        alias="ISOCHRONE_REQUEST_TIMEOUT",
        description="HTTP timeout applied to OTP calls",
    )
    request_retries: PositiveInt = Field(
        3,
        alias="ISOCHRONE_REQUEST_RETRIES",
        description="Number of retry attempts for transient OTP failures",
    )
    request_backoff_seconds: PositiveFloat = Field(
        0.5,
        alias="ISOCHRONE_REQUEST_BACKOFF",
        description="Base backoff delay between retries",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

