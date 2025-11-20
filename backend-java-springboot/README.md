# Backend Java (Spring Boot)

Java 21 + Spring Boot 3 기반 Isochrone API 래퍼입니다. OTP 컨테이너(`/otp/routers/default/isochrone`)에 대한 HTTP 요청을 래핑하고, 입력 검증과 예외 처리를 담당합니다.

## 실행 방법

```bash
# 프로젝트 루트에서 백엔드만 실행
cd backend-java
./gradlew bootRun
```

Docker Compose 환경에서는 `backend-java-springboot` 서비스가 자동으로 빌드되고 실행되지만, 기본 설정에서는 외부 포트를 노출하지 않습니다. 필요 시 compose override를 사용하거나 로컬에서 직접 `bootRun`을 실행하여 접근하세요.

## 환경 변수

- `OTP_API_BASE_URL` (기본값 `http://otp:8080/otp`): OTP 컨테이너의 베이스 URL
- `SPRING_PROFILES_ACTIVE` (선택): Spring profile

## API 호출 예시

```bash
curl "http://localhost:8080/api/isochrone?fromPlace=37.5665,126.9780&cutoffSec=1800&mode=TRANSIT"
```

## Swagger / OpenAPI

- JSON 스키마: `http://localhost:8080/v3/api-docs`
- UI: `http://localhost:8080/swagger-ui/index.html`

## 테스트

```bash
./gradlew test
```
