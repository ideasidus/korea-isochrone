# 대중교통 기반 부동산 교통 접근성 분석 플랫폼 PRD

## Overview

**제품명**: N분도착 - 대중교통 기반 부동산 교통 접근성 분석 플랫폼

**문제 정의**:
현재 부동산 시장에서는 교통 접근성을 평가할 때 단순한 직선 거리나 주관적 판단에 의존하고 있습니다. 실제 대중교통을 이용한 이동 시간과 도달 가능 범위를 정확히 파악하기 어려워, 투자자와 거주자들이 잘못된 의사결정을 내리는 경우가 빈번합니다.

**솔루션**:
한국 GTFS(General Transit Feed Specification) 데이터와 OpenStreetMap을 활용하여 실시간 대중교통 이동 시간 기반의 Isochrone Map을 생성하고, 이를 부동산 정보와 연계하여 정확한 교통 접근성 분석을 제공하는 플랫폼입니다.

**대상 사용자**:

- 부동산 투자자 및 중개업체
- 주거지 선택을 고민하는 일반 소비자  
- 도시 계획 및 교통 정책 관련 공공기관
- 부동산 플랫폼 및 PropTech 스타트업

**핵심 가치**:

- **정확성**: 실제 대중교통 시간표 기반의 정밀한 이동 시간 계산
- **효율성**: 기존 GraphHopper 대비 60% 빠른 계산 속도 (60초 → 15-25초)
- **경제성**: 메모리 사용량 60% 절약으로 인프라 비용 최적화
- **확장성**: 서울에서 전국 단위로 확장 가능한 아키텍처

## Core Features

### 1. Isochrone Map 생성 엔진

**기능**: 특정 지점에서 N분(15분, 30분, 45분, 60분) 내 대중교통으로 도달 가능한 범위를 지도 상에 시각화
**중요성**: 플랫폼의 핵심 기능으로, 정확한 교통 접근성 데이터 제공의 기반
**동작 방식**:

- OpenTripPlanner 기반 RAPTOR 알고리즘 활용
- 한국 GTFS 데이터와 OSM 데이터 통합 처리
- REST API를 통한 실시간 계산 및 결과 반환

### 2. 부동산-교통 접근성 연계 분석

**기능**: 특정 부동산 물건의 주요 목적지(강남역, 여의도, 판교 등)까지의 대중교통 접근성 점수 계산
**중요성**: 단순한 시각화를 넘어 실용적인 의사결정 지원 도구 제공
**동작 방식**:

- 사전 정의된 주요 비즈니스 허브까지의 이동 시간 계산
- 환승 횟수, 도보 시간 등을 고려한 종합 접근성 점수 산출
- 비교 분석 및 랭킹 기능 제공

### 3. 캐싱 및 성능 최적화 시스템

**기능**: 자주 요청되는 지점의 isochrone 결과를 캐싱하여 응답 시간 단축
**중요성**: 실시간 서비스 제공을 위한 필수 기능
**동작 방식**:

- Redis 기반 결과 캐싱 (TTL: 1시간)
- 격자 기반 사전 계산 isochrone 저장
- 지능형 캐시 무효화 전략

### 4. RESTful API 서비스

**기능**: 외부 시스템에서 isochrone 데이터를 활용할 수 있는 API 인터페이스 제공
**중요성**: 플랫폼의 확장성과 다양한 서비스와의 연동을 위한 기반
**동작 방식**:

- GraphQL 또는 REST API를 통한 표준화된 데이터 제공
- Rate limiting 및 API 키 기반 접근 제어
- 다양한 출력 형식 지원 (GeoJSON, 이미지 등)

## User Experience

### User Personas

**1. 부동산 투자자 (김투자, 35세)**

- 목표: 교통 접근성이 좋은 수익성 높은 부동산 발굴
- 사용 패턴: 특정 지역의 여러 매물을 동시에 비교 분석
- 주요 관심사: 강남, 여의도 등 주요 비즈니스 지구까지의 출퇴근 편의성

**2. 주거지 탐색자 (이직장, 28세)**  

- 목표: 회사까지 출퇴근이 편리한 거주지 탐색
- 사용 패턴: 회사 위치 기준으로 30-45분 내 통근 가능 지역 확인
- 주요 관심사: 실제 이동 시간, 환승 횟수, 막차 시간

**3. 부동산 중개업체 (박중개, 42세)**

- 목표: 고객에게 객관적이고 정확한 교통 접근성 정보 제공
- 사용 패턴: 매물 소개 시 시각적 자료로 활용
- 주요 관심사: 신뢰성 있는 데이터, 쉬운 시각화

### Key User Flows

**1. 기본 Isochrone 조회 플로우**

1. 지도에서 시작점 선택 또는 주소 입력
2. 이동 시간 선택 (15/30/45/60분)
3. 대중교통 옵션 설정 (지하철만/버스포함/도보연계)
4. Isochrone 계산 및 지도 시각화
5. 결과 저장 또는 공유

**2. 부동산 비교 분석 플로우**

1. 비교할 부동산 위치들을 지도에 추가
2. 공통 목적지(직장, 학교 등) 설정  
3. 각 부동산별 접근성 점수 계산
4. 비교 테이블 및 차트로 결과 제시
5. 상세 분석 보고서 생성

### UI/UX 고려사항

**1. 직관적인 지도 인터페이스**

- 대화형 지도 기반의 시각적 조작
- 색상 그라데이션을 통한 이동 시간 구간 표시
- 실시간 계산 진행상황 표시

**2. 반응형 웹 디자인**  

- 모바일, 태블릿, 데스크톱 환경 지원
- 터치 기반 지도 조작 최적화

**3. 성능 중심 UX**

- 계산 중 로딩 인디케이터와 예상 소요 시간 표시
- 점진적 결과 로딩 (부분 결과부터 표시)
- 오프라인 캐시 활용

## Technical Architecture

### System Components

**1. 코어 Isochrone 엔진**

- **OpenTripPlanner 2.2+**: RAPTOR 알고리즘 기반 경로 탐색
- **Docker 컨테이너**: 격리된 환경에서의 안정적 실행
- **JVM 최적화**: G1GC, 힙 메모리 8-12GB 할당

**2. 데이터 레이어**

- **GTFS 데이터**: 한국 전국 대중교통 시간표 데이터
- **OpenStreetMap**: 도로망 및 POI 데이터
- **PostgreSQL + PostGIS**: 공간 데이터 저장 및 쿼리
- **Redis**: 실시간 캐싱 및 세션 관리

**3. 웹 애플리케이션 레이어**

- **Spring Boot**: RESTful API 서버
- **React.js**: 프론트엔드 SPA
- **Leaflet/MapboxGL**: 지도 시각화
- **WebSocket**: 실시간 계산 진행상황 통신

**4. 인프라 레이어**

- **Docker Compose**: 멀티 컨테이너 오케스트레이션
- **Nginx**: 리버스 프록시 및 정적 파일 서빙
- **Oracle Cloud ARM**: 호스팅 인프라 (4코어, 24GB RAM)

### Data Models

**1. Isochrone Request**

```
{
  "origin": {"lat": 37.5665, "lng": 126.9780},
  "travelTime": 3600,
  "mode": ["TRANSIT", "WALK"],
  "departure": "2025-10-12T09:00:00+09:00",
  "walkSpeed": 1.4
}
```

**2. Isochrone Response**  

```
{
  "id": "iso_123456",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[lng, lat], ...]]
  },
  "properties": {
    "travelTime": 3600,
    "calculationTime": 23.5,
    "coverage": 0.85
  }
}
```

**3. Accessibility Score**

```
{
  "propertyId": "prop_789",
  "destinations": [
    {
      "name": "강남역",
      "travelTime": 1800,
      "transfers": 1,
      "score": 8.5
    }
  ],
  "overallScore": 7.8
}
```

### APIs and Integrations

**1. 핵심 API 엔드포인트**

- `POST /api/v1/isochrone` - Isochrone 계산 요청
- `GET /api/v1/isochrone/{id}` - 계산 결과 조회
- `POST /api/v1/accessibility/analyze` - 접근성 분석
- `GET /api/v1/properties/{id}/accessibility` - 부동산 접근성 정보

**2. 외부 데이터 연동**

- 국가교통DB: GTFS 데이터 정기 업데이트
- 공공데이터포털: 부동산 실거래가 데이터
- OpenStreetMap: 지도 데이터 동기화

### Infrastructure Requirements

**1. 최소 시스템 요구사항**

- CPU: 4코어 이상
- RAM: 16GB (JVM 8GB + 시스템 8GB)
- Storage: 100GB SSD (GTFS + OSM 데이터)
- Network: 100Mbps 이상

**2. 권장 프로덕션 환경**

- CPU: 8코어 (ARM64 또는 x86_64)
- RAM: 32GB (JVM 16GB + 캐시 8GB + 시스템 8GB)  
- Storage: 200GB NVMe SSD
- Network: 1Gbps 이상

## Development Roadmap

### Phase 1: MVP - 핵심 Isochrone 엔진 (POC)

**범위**: 기본적인 isochrone 계산 및 시각화 기능
**구현 요소**:

- OpenTripPlanner 설치 및 한국 GTFS 데이터 통합
- Docker 기반 배포 환경 구성
- 단일 지점 isochrone 계산 API
- 기본 웹 인터페이스 (지도 + 계산 폼)
- 메모리 최적화 및 성능 튜닝

**핵심 기능**:

- 서울 강남 지역 기준 60분 isochrone 계산
- REST API 기본 엔드포인트 제공
- 지도 기반 시각화
- 계산 시간 15-25초 달성

### Phase 2: Enhancement - 성능 최적화 및 캐싱

**범위**: 실용적 성능과 사용자 경험 개선
**구현 요소**:

- Redis 기반 결과 캐싱 시스템
- 다중 시간대 isochrone 동시 계산
- 계산 진행상황 실시간 표시
- 사전 계산된 격자 기반 isochrone 저장
- API 응답 최적화 (압축, 부분 로딩)

**핵심 기능**:

- 캐싱된 결과 3초 이내 응답
- 15/30/45/60분 다중 isochrone 표시
- 계산 대기열 관리
- 자주 사용되는 지점 사전 계산

### Phase 3: Integration - 부동산 데이터 연계

**범위**: 부동산 정보와 교통 접근성 통합 분석
**구현 요소**:

- 부동산 실거래가 데이터 API 연동
- 주요 비즈니스 허브 데이터베이스 구축
- 접근성 점수 계산 알고리즘
- 부동산 비교 분석 인터페이스
- 보고서 생성 및 내보내기 기능

**핵심 기능**:

- 매물별 교통 접근성 점수 자동 계산
- 여러 매물 동시 비교 분석
- 주요 목적지까지 소요 시간 및 경로 정보
- 상세 분석 보고서 PDF 생성

### Phase 4: Scale - 전국 확장 및 고도화

**범위**: 서비스 규모 확장 및 고급 기능 추가
**구현 요소**:

- 전국 GTFS 데이터 통합 처리
- 멀티 인스턴스 부하 분산
- 실시간 GTFS-RT 데이터 적용
- 머신러닝 기반 이동 패턴 예측
- 모바일 앱 개발

**핵심 기능**:

- 전국 단위 isochrone 서비스
- 실시간 교통상황 반영
- 개인화된 통근 패턴 분석
- 부동산 투자 추천 시스템

## Logical Dependency Chain

### 1. Foundation Layer (최우선 구축)

**필수 선행 요소**:

- Java 17 + Docker 개발 환경 구성
- 한국 GTFS 데이터 수집 및 전처리
- OpenTripPlanner 설치 및 그래프 빌드
- 기본 Docker Compose 설정

**이유**: 모든 기능의 기반이 되는 핵심 엔진 없이는 아무것도 시작할 수 없음

### 2. Quick Win - 최소 기능 프론트엔드 (빠른 가시성)

**구현 범위**:

- 단일 지점 isochrone 계산 API 1개
- 기본 지도 인터페이스 (Leaflet 기반)
- 하드코딩된 테스트 지점들 (강남역, 홍대입구역 등)
- 결과 시각화 (단순 폴리곤 표시)

**목표**: 2주 내에 동작하는 데모 버전 완성으로 개념 검증

### 3. Atomic Feature Development (단계적 기능 확장)

**3.1 API 안정화**

- 에러 핸들링 및 유효성 검사
- API 문서화 (Swagger)
- 기본 로깅 시스템

**3.2 성능 최적화**  

- JVM 튜닝 및 메모리 최적화
- 기본 결과 캐싱 (메모리 기반)
- 계산 시간 모니터링

**3.3 사용자 경험 개선**

- 동적 지점 선택 (클릭/주소 검색)
- 다중 시간대 선택 UI
- 계산 진행상황 표시

**3.4 데이터 확장**

- 서울 외 수도권 데이터 추가
- 부동산 기본 정보 연동
- 주요 POI 데이터베이스 구축

### 4. Integration & Enhancement (통합 및 고도화)

**순서별 우선순위**:

1. Redis 캐싱 시스템 (성능 크리티컬)
2. 부동산 실거래가 API 연동 (핵심 가치)
3. 접근성 점수 계산 로직 (차별화 요소)
4. 비교 분석 기능 (사용성)
5. 보고서 생성 (부가 가치)

### 5. Production Readiness (운영 준비)

**마지막 단계 요소들**:

- API Rate limiting 및 보안
- 에러 모니터링 및 알람
- 백업 및 복구 시스템
- 성능 모니터링 대시보드

## Risks and Mitigations

### Technical Challenges

**1. 대용량 GTFS 데이터 처리 성능**

- **위험도**: High
- **영향**: 메모리 부족으로 인한 서비스 중단, 계산 시간 지연
- **완화 방안**:
  - 단계적 데이터 로딩 (서울 → 수도권 → 전국)
  - 메모리 사용량 실시간 모니터링 및 알람
  - 그래프 분할 및 로드밸런싱 준비

**2. OpenTripPlanner 학습 곡선**

- **위험도**: Medium  
- **영향**: 개발 일정 지연, 최적화 미흡
- **완화 방안**:
  - OTP 커뮤니티 활용 및 문서 정독
  - 간단한 테스트 케이스부터 점진적 확장
  - 외부 전문가 자문 고려

**3. 한국 GTFS 데이터 품질 이슈**

- **위험도**: Medium
- **영향**: 부정확한 계산 결과, 사용자 신뢰도 하락
- **완화 방안**:
  - 데이터 검증 파이프라인 구축
  - 알려진 이슈들에 대한 수동 보정
  - 사용자 피드백 수집 및 개선

### MVP 정의 및 구축 전략

**1. 과도한 기능 욕심**

- **위험도**: High
- **영향**: MVP 완성 지연, 리소스 분산
- **완화 방안**:
  - "강남역 기준 60분 isochrone 계산"을 최소 성공 기준으로 설정
  - 기능 추가는 Phase 방식으로 엄격히 관리
  - 매주 동작하는 버전 유지 원칙

**2. 완벽주의 함정**

- **위험도**: Medium
- **영향**: 출시 시점 지연, 시장 검증 기회 상실
- **완화 방안**:
  - "80% 완성도에서 출시" 원칙
  - 사용자 피드백 기반 개선 우선
  - MVP 이후 지속적 개선 문화

### Resource Constraints

**1. 단일 서버 환경의 한계**

- **위험도**: Medium
- **영향**: 트래픽 증가 시 성능 저하, 확장성 제약
- **완화 방안**:
  - 수직 확장(Scale-up) 우선 고려
  - 캐싱을 통한 부하 분산
  - 향후 수평 확장을 위한 아키텍처 준비

**2. 무료 인프라의 제약**

- **위험도**: Low
- **영향**: 상용 서비스 전환 시 추가 비용 발생
- **완화 방안**:
  - Oracle Cloud 평생무료 한도 내 최적화
  - 비용 모니터링 및 예산 계획
  - 수익 모델 검증 후 유료 플랜 전환

**3. GTFS 데이터 업데이트 지연**

- **위험도**: Low
- **영향**: 최신 교통 정보 반영 지연
- **완화 방안**:
  - 반자동 데이터 업데이트 파이프라인 구축
  - 데이터 갱신 주기 명시 및 사용자 안내
  - 수동 업데이트 프로세스 준비

## Appendix

### Research Findings

**1. GraphHopper vs OpenTripPlanner 성능 비교**

- GraphHopper: 60초 계산 시간, 20GB 메모리 사용
- OpenTripPlanner: 15-25초 예상, 8-12GB 메모리 사용
- 메모리 효율성 60% 개선, 계산 성능 60% 개선 예상

**2. 한국 GTFS 데이터 현황**

- 전국 대중교통 노선 정보 포함
- timezone 수정 필요 (Korea → Asia/Seoul)
- 실시간 GTFS-RT 데이터는 제한적 제공

**3. 시장 조사 결과**

- 부동산 플랫폼들의 교통 접근성 정보는 대부분 부정확
- 직선 거리 기반 정보 제공이 일반적
- 정확한 대중교통 이동 시간 수요 존재

### Technical Specifications

**1. 하드웨어 요구사항**

```
Minimum:
  CPU: 4 cores (ARM64 or x86_64)
  RAM: 16GB
  Storage: 100GB SSD
  Network: 100Mbps

Recommended:
  CPU: 8 cores
  RAM: 32GB  
  Storage: 200GB NVMe SSD
  Network: 1Gbps
```

**2. 소프트웨어 스택**

```
Backend:
  - OpenTripPlanner 2.2+
  - Java 17 (OpenJDK)
  - Spring Boot 3.x
  - PostgreSQL 15 + PostGIS
  - Redis 7.x

Frontend:
  - React 18
  - TypeScript
  - Leaflet/MapboxGL
  - Tailwind CSS

Infrastructure:
  - Docker & Docker Compose
  - Nginx
  - Oracle Cloud ARM
```

**3. API 사양**

```
Base URL: https://api.transitmap.kr/v1

Authentication: 
  - API Key (Header: X-API-Key)
  - Rate Limit: 100 requests/hour

Response Format: JSON
Supported Output: GeoJSON, PNG, SVG
```

**4. 데이터 소스**

```
Transportation Data:
  - 국가교통DB GTFS 데이터
  - OpenStreetMap 한국 데이터
  - 실시간 GTFS-RT (선택적)

Real Estate Data:
  - 국토교통부 실거래가 공개시스템
  - 공공데이터포털 부동산 정보

POI Data:
  - 주요 비즈니스 허브 (강남, 여의도, 판교 등)
  - 교육시설, 의료시설, 쇼핑센터
```
