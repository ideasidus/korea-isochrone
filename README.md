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

## Isochrone API 사용법

FastAPI 백엔드를 통해 대중교통 등시선(Isochrone)을 생성할 수 있습니다.

### 엔드포인트

```
GET http://localhost:8000/api/v1/isochrone
```

### 요청 파라미터

| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|------|------|------|
| `lat` | float | ✅ | 출발 위도 (-90 ~ 90) | `37.5665` |
| `lon` | float | ✅ | 출발 경도 (-180 ~ 180) | `126.9780` |
| `cutoffMin` | integer | ✅ | 최대 이동 시간 (분 단위) | `30` (30분) |
| `modes` | array[string] | ❌ | 이동 수단 목록 (기본값: `WALK,TRANSIT`) | `WALK`, `TRANSIT`, `BICYCLE`, `CAR` |
| `arriveBy` | boolean | ❌ | 도착 시간 기준 여부 (기본값: `false`) | `false` |

#### 이동 수단 (Transport Modes)

| 값 | 설명 |
|----|------|
| `WALK` | 도보 |
| `TRANSIT` | 대중교통 (버스, 지하철 등) |
| `BICYCLE` | 자전거 |
| `CAR` | 자동차 |

**참고**: `modes` 파라미터는 여러 값을 쉼표로 구분하여 전달할 수 있습니다 (예: `WALK,TRANSIT`).

### 응답 형식

GeoJSON FeatureCollection 형식으로 등시선 폴리곤을 반환합니다.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "time": "1800"
      },
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [...]
      }
    }
  ]
}
```

### 사용 예시

**서울 시청 기준 30분 대중교통 등시선:**
```bash
curl "http://localhost:8000/api/v1/isochrone?lat=37.5665&lon=126.9780&cutoffMin=30"
```

**강남역 기준 60분 대중교통 등시선:**
```bash
curl "http://localhost:8000/api/v1/isochrone?lat=37.4979&lon=127.0276&cutoffMin=60"
```

**자전거 전용 30분 등시선:**
```bash
curl "http://localhost:8000/api/v1/isochrone?lat=37.5665&lon=126.9780&cutoffMin=30&modes=BICYCLE"
```

**도보 + 대중교통 복합 이동 45분 등시선:**
```bash
curl "http://localhost:8000/api/v1/isochrone?lat=37.4979&lon=127.0276&cutoffMin=45&modes=WALK,TRANSIT"
```

### 기술 스택

- **OTP 버전**: 2.5.0
- **API 유형**: TravelTime Sandbox API (`/otp/traveltime/isochrone`)
- **지원 모드**: WALK, TRANSIT (대중교통)
- **데이터**: 한국 전국 OSM + GTFS

### 에러 응답

**422 Unprocessable Entity**: 잘못된 파라미터 또는 검증 실패
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "lat"],
      "msg": "Field required"
    }
  ]
}
```

**파라미터 범위 오류 (위도/경도 범위 초과):**
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["query", "lat"],
      "msg": "Input should be less than or equal to 90"
    }
  ]
}
```

**502 Bad Gateway**: OTP 서비스 연결 실패
```json
{
  "detail": "OTP 서비스에 연결할 수 없습니다"
}
```
