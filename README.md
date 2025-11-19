# Korea Isochrone – OTP 운영 가이드

이 저장소는 OpenTripPlanner(OTP) 2.8.1 공식 컨테이너 이미지를 이용해 한국 GTFS/OSM 데이터를 기반으로 등시선(Isochrone) API를 제공하기 위한 Docker 구성을 포함합니다. 외부에서 수동으로 확보한 데이터를 `otp/data/` 에 배치한 뒤, `graph-builder` 서비스로 그래프를 생성하고 `otp` 서비스로 API를 제공하는 구조입니다.

## 사전 준비

1. **필수 도구**
   - Docker 24+
   - Docker Compose v2 (`docker compose` 명령 사용)

2. **데이터 배치**
   - `otp/data/` 디렉터리에 다음 파일을 수동으로 복사합니다.
     - GTFS ZIP (파일명에 `gtfs` 문자열 포함 권장, 예: `south-korea-gtfs.zip`)
     - OSM PBF (예: `south-korea-latest.osm.pbf`)
   - 대용량 파일은 Git에 포함되지 않으므로 필요 시 별도 저장소/스토리지에서 내려받아 이 디렉터리에 배치합니다.

## 사용 방법

### 1. 그래프 빌드

그래프 파일(`otp/graph.obj`)이 없거나 데이터를 갱신한 경우 아래 명령으로 새 그래프를 생성합니다. 데이터 규모에 따라 수 시간 동안 메모리 16GB 이상이 필요할 수 있습니다.

```bash
docker compose run --rm graph-builder
```

빌드가 완료되면 `otp/graph.obj` 파일이 생성되며, 이후 서버는 이 파일을 로드해 실행합니다.

### 2. OTP 서버 + Spring Boot 래퍼 실행

그래프가 준비된 상태에서 OTP 서버와 Spring Boot 백엔드 래퍼(`backend-java` 서비스)를 함께 실행합니다. 기본 설정에서는 어떤 컨테이너도 호스트 포트를 노출하지 않으며, 서비스 간 통신은 Docker 네트워크 내부에서만 이루어집니다.

```bash
docker compose up -d
```

헬스 체크:

```bash
# OTP 컨테이너 내부 엔드포인트
docker compose exec otp curl -s http://otp:8080/otp/routers/default/health

# Spring Boot 백엔드 호출 (backend-java 컨테이너 안에서 실행)
docker compose exec backend-java curl "http://localhost:8080/api/isochrone?fromPlace=37.5665,126.9780&cutoffSec=1800"
```

서버 중지는 다음과 같이 수행합니다.

```bash
docker compose down
```

### 3. 백엔드 개발/테스트

`backend-java/` 디렉터리는 Java 21 + Spring Boot 3 기반의 Isochrone API 래퍼를 포함합니다.

```bash
cd backend-java
./gradlew bootRun              # 로컬 실행
./gradlew test                 # 단위 테스트
```

개발 서버를 로컬에서 띄운 경우에는 `http://localhost:8080/api/isochrone?...` 로 직접 호출할 수 있습니다. Docker Compose 환경에서는 컨테이너가 포트를 노출하지 않으므로 `docker compose exec backend-java`와 `curl`을 조합해 호출하거나, 필요 시 override 파일을 만들어 포트를 노출하세요. OTP 주소(`http://otp:8080/otp`)는 `application.yml` 혹은 `OTP_API_BASE_URL` 환경 변수로 조정합니다.

#### Swagger / OpenAPI 문서

Springdoc OpenAPI를 사용하여 자동 문서를 제공합니다.

- JSON 스키마: `http://localhost:8080/v3/api-docs`
- Swagger UI: `http://localhost:8080/swagger-ui/index.html`

Docker Compose 환경에서도 동일하게 접근 가능합니다.

### 4. 로그 확인

그래프 빌드나 서버 실행 중 상태를 실시간으로 확인하려면:

```bash
docker compose logs -f graph-builder   # 빌드 중
docker compose logs -f otp             # 서버 실행 중
```

## 디렉터리 구조 요약

```
otp/
├── build-config.json    # OSM/GTFS 소스 경로 정의
├── router-config.json   # 라우팅 기본값
├── graph.obj            # graph-builder 실행 후 생성 (Git 무시 대상)
└── data/
    ├── south-korea-gtfs.zip
    └── south-korea-latest.osm.pbf
```

## 참고 사항

- `docker-compose.yml`에는 `otp`(로드/서버), `graph-builder`(빌드/저장), `backend-java`(Spring Boot 래퍼) 서비스가 정의되어 있습니다.
- 그래프를 다시 빌드하지 않는 한 `otp`와 `backend-java` 서비스만 실행하면 됩니다.
- `otp/graph.obj`는 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.
