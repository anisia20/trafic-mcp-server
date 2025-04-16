```markdown
# Traffic Monitoring System Documentation

## 시스템 구성
- **Server URL:** [http://localhost:8000/sse](http://localhost:8000/sse)
- **MCP Server Configuration:** 서버 설정은 `mcp.json` 파일에 정의되어 있습니다.

## 기능
- **트래픽 알림 조회 (get_alerts)**
  - 트래픽 상황을 지역별로 모니터링하고, 해당 지역의 교통 알림 정보를 실시간으로 확인할 수 있습니다.

## 요청 형식
요청은 JSON 형식으로 전송됩니다. 예를 들어, 특정 지역의 트래픽 정보를 요청하려면 아래와 같이 전달할 수 있습니다:

```json
{
  "state": "seoul"
}
```

## 사용 방법

### 1. 서버 실행 확인
- 우선 Traffic Monitoring 서버가 실행 중인지 확인합니다.
- 서버 주소: [http://localhost:8000/sse](http://localhost:8000/sse)

### 2. 알림 요청
- 원하는 지역명을 지정하여 트래픽 정보를 요청합니다.
- 예를 들어 "seoul" 지역의 트래픽 정보를 요청하면, 해당 지역의 알림 정보가 반환됩니다.

## 시스템 요구사항
- **서버 실행 환경:** 해당 시스템을 실행할 수 있는 서버 환경이 필요합니다.
- **API 접근 권한:** API에 접근할 수 있는 적절한 권한이 필요합니다.

## 주의사항
- Traffic Monitoring 서버가 실행 중이어야 데이터 조회가 가능합니다.
- 요청 시 올바른 지역명을 입력해야 합니다.
- 실시간 트래픽 정보 모니터링으로 데이터가 지속적으로 업데이트 됩니다.

## 설정 파일
- 서버 설정 및 관련 구성은 `mcp.json` 파일 내에서 관리됩니다.
```
