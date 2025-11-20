# Backend Python (FastAPI)

FastAPI + httpx 기반 Isochrone 래퍼로, 내부 Docker 네트워크(`isochrone-internal`)를 통해 OTP(`http://otp:8080/otp`)에 요청을 프록시합니다.

## 로컬 개발

필요 도구: [uv](https://github.com/astral-sh/uv) 0.9+, Python 설치 권한 없는 환경을 위해 캐시 경로를 workspace 내로 지정합니다.

```bash
cd backend
UV_CACHE_DIR=../.uv-cache UV_PYTHON_INSTALL_DIR=../.uv-python uv sync

# 개발 서버
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# 테스트
uv run pytest
```

환경 변수(기본값은 `app/config.py` 참고):

| 이름 | 기본값 | 설명 |
| --- | --- | --- |
| `OTP_API_BASE_URL` | `http://otp:8080/otp` | OTP REST 엔드포인트 (OTP 공식 문서에서 `/otp/...` 경로 사용[^otp-base]) |
| `OTP_ROUTER_ID` | `default` | OTP 라우터 ID |
| `ISOCHRONE_REQUEST_TIMEOUT` | `10` | httpx 요청 타임아웃 |
| `ISOCHRONE_REQUEST_RETRIES` | `3` | 재시도 횟수 |
| `ISOCHRONE_REQUEST_BACKOFF` | `0.5` | 재시도 백오프 초 |

FastAPI는 기본 Swagger UI를 제공합니다.

- JSON: `http://localhost:8080/openapi.json`
- Swagger UI: `http://localhost:8080/docs`

## Docker Compose

`docker-compose.yml`의 `backend-python-fastapi` 서비스가 이 모듈을 빌드 및 실행합니다. 기본적으로 호스트 `8080` 포트를 `uvicorn` 포트(8000)에 바인딩하므로, `docker compose up backend-python-fastapi` 실행 후 `http://localhost:8080/api/isochrone?...`으로 접근하면 OTP 응답을 받을 수 있습니다.

[^otp-base]: OpenTripPlanner Transmodel GraphQL 문서(`doc/user/apis/TransmodelApi.md`)에서는 로컬 엔드포인트를 `http://localhost:8080/otp/transmodel/v3`와 같이 `/otp` 프리픽스로 안내합니다. 동일한 기준을 사용해 OTP Base URL을 설정합니다.
