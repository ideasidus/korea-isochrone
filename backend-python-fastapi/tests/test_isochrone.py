import os

import httpx
import pytest
import respx

from app.config import get_settings
from app.main import create_app


@pytest.fixture(autouse=True)
def configure_env():
    os.environ["OTP_API_BASE_URL"] = "http://otp:8080/otp"
    os.environ["ISOCHRONE_REQUEST_RETRIES"] = "2"
    os.environ["ISOCHRONE_REQUEST_TIMEOUT"] = "5"
    os.environ["ISOCHRONE_REQUEST_BACKOFF"] = "0.01"
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_isochrone_proxy_success():
    app = create_app()
    with respx.mock(base_url="http://otp:8080/otp") as mock_router:
        mock_router.get("/routers/default/isochrone").mock(
            return_value=httpx.Response(
                status_code=200,
                json={"type": "FeatureCollection", "features": []},
            )
        )

        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get(
                "/api/isochrone",
                params={"fromPlace": "37.5665,126.9780", "cutoffSec": 600},
            )

    assert response.status_code == 200
    assert response.json()["type"] == "FeatureCollection"


@pytest.mark.asyncio
async def test_isochrone_proxy_translates_errors():
    app = create_app()
    with respx.mock(base_url="http://otp:8080/otp") as mock_router:
        mock_router.get("/routers/default/isochrone").mock(
            return_value=httpx.Response(status_code=400, json={"error": "invalid"})
        )

        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get(
                "/api/isochrone",
                params={"fromPlace": "37.5665,126.9780", "cutoffSec": 300},
            )

    assert response.status_code == 400
    assert response.json()["detail"].startswith("OTP 요청이 실패했습니다")

