import os

import httpx
import pytest
import respx

from app.config import get_settings
from app.main import create_app
from app.schemas.isochrone import TransportMode


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
async def test_isochrone_success_with_default_modes():
    """기본 이동 수단(WALK, TRANSIT)으로 등시선 요청 성공 테스트"""
    app = create_app()
    with respx.mock(base_url="http://otp:8080/otp") as mock_router:
        # OTP 2.5.0 TravelTime API endpoint
        mock_router.get("/traveltime/isochrone").mock(
            return_value=httpx.Response(
                status_code=200,
                json={"type": "FeatureCollection", "features": []},
            )
        )

        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get(
                "/api/v1/isochrone",
                params={"lat": 37.5665, "lon": 126.9780, "cutoffMin": 10},
            )

    assert response.status_code == 200
    assert response.json()["type"] == "FeatureCollection"


@pytest.mark.asyncio
async def test_isochrone_success_with_custom_modes():
    """커스텀 이동 수단으로 등시선 요청 성공 테스트"""
    app = create_app()
    with respx.mock(base_url="http://otp:8080/otp") as mock_router:
        mock_router.get("/traveltime/isochrone").mock(
            return_value=httpx.Response(
                status_code=200,
                json={
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {"time": "1800"},
                            "geometry": {"type": "MultiPolygon", "coordinates": []},
                        }
                    ],
                },
            )
        )

        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get(
                "/api/v1/isochrone",
                params={
                    "lat": 37.4979,
                    "lon": 127.0276,
                    "cutoffMin": 30,
                    "modes": [TransportMode.WALK.value, TransportMode.BICYCLE.value],
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1


@pytest.mark.asyncio
async def test_isochrone_translates_otp_errors():
    """OTP 에러를 FastAPI 에러로 변환하는 테스트"""
    app = create_app()
    with respx.mock(base_url="http://otp:8080/otp") as mock_router:
        mock_router.get("/traveltime/isochrone").mock(
            return_value=httpx.Response(status_code=400, json={"error": "invalid"})
        )

        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get(
                "/api/v1/isochrone",
                params={"lat": 37.5665, "lon": 126.9780, "cutoffMin": 5},
            )

    assert response.status_code == 400
    assert response.json()["detail"].startswith("OTP 요청이 실패했습니다")


@pytest.mark.asyncio
async def test_isochrone_validation_invalid_latitude():
    """잘못된 위도 값 검증 테스트"""
    app = create_app()

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        # 위도 범위를 벗어난 값 (>90)
        response = await client.get(
            "/api/v1/isochrone",
            params={"lat": 100.0, "lon": 126.9780, "cutoffMin": 10},
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("lat" in str(error["loc"]) for error in detail)


@pytest.mark.asyncio
async def test_isochrone_validation_invalid_longitude():
    """잘못된 경도 값 검증 테스트"""
    app = create_app()

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        # 경도 범위를 벗어난 값 (<-180)
        response = await client.get(
            "/api/v1/isochrone",
            params={"lat": 37.5665, "lon": -200.0, "cutoffMin": 10},
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("lon" in str(error["loc"]) for error in detail)


@pytest.mark.asyncio
async def test_isochrone_validation_missing_required_params():
    """필수 파라미터 누락 테스트"""
    app = create_app()

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        # lat 파라미터 누락
        response = await client.get(
            "/api/v1/isochrone",
            params={"lon": 126.9780, "cutoffMin": 10},
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("lat" in str(error["loc"]) for error in detail)
