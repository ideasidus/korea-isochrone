# Korea Isochrone – OTP 운영 가이드

OpenTripPlanner(OTP) 2.8.1 컨테이너와 여러 백엔드 래퍼(Spring Boot, FastAPI)를 하나의 Docker Compose 스택으로 관리합니다. GTFS/OSM 데이터를 `otp/data/`에 배치하고 그래프를 생성한 뒤, 원하는 백엔드를 통해 Isochrone API를 노출할 수 있습니다.

## 준비 사항

- Docker 24+
- Docker Compose v2 (`docker compose`)
- 데이터 배치: `otp/data/`에 GTFS ZIP, OSM PBF 등을 사전에 복사합니다.

## 그래프 빌드

그래프(`otp/graph.obj`)가 없거나 데이터를 갱신해야 할 때 실행합니다.

```bash
docker compose run --rm graph-builder
```

빌드가 끝나면 `otp/graph.obj`가 생성되며 이후 `otp` 서비스가 자동으로 로드합니다.

## 서비스 실행과 헬스 체크

```bash
docker compose up -d

# OTP 상태 확인
docker compose exec otp curl -s http://otp:8080/otp/routers/default/health
```

특정 백엔드만 기동하고 싶다면 서비스 이름을 지정합니다.

```bash
docker compose up -d backend-java-springboot
docker compose up -d backend-python-fastapi
```

로그 확인:

```bash
docker compose logs -f graph-builder
docker compose logs -f otp
```

## 백엔드 옵션

| 서비스 | 설명 | 포트 노출 | 문서 |
| --- | --- | --- | --- |
| `backend-java-springboot` | Java 21 + Spring Boot 3 래퍼 | 기본적으로 내부 통신 전용 | `backend-java/README.md` |
| `backend-python-fastapi` | FastAPI + httpx 래퍼 | 호스트 `8080` 바인딩 | `backend/README.md` |

필요한 백엔드의 설정/개발 워크플로우는 각 디렉터리 README에서 확인하세요.

## 디렉터리 개요

```
otp/                 # build-config, router-config, 데이터
backend-java/        # Spring Boot 래퍼 (독립 README 포함)
backend/             # FastAPI 래퍼 (독립 README 포함)
docker-compose.yml   # 공용 스택 정의
```

공통 사항:

- `isochrone-internal` Docker 네트워크에서 OTP와 백엔드가 통신합니다.
- `otp/graph.obj`는 `.gitignore`에 포함되며 필요 시 `graph-builder`로 재생성합니다.
