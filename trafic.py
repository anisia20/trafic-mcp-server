from typing import Any
import logging
import httpx
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# FastMCP 서버 초기화
mcp = FastMCP("trafic")

# 상수
NWS_API_BASE = (
    "https://www.utic.go.kr/tsdms/incident.do?sidoCd=11&gugunCd=&accident_gubun=%7B%22%EC%82%AC%EA%B3%A0%22%3A%22A0401%2CA0402%2CA0403%22%2C%22%EA%B3%B5%EC%82%AC%22%3A%22%22%2C%22%ED%96%89%EC%82%AC%22%3A%22%22%2C%22%EA%B8%B0%EC%83%81%22%3A%22%22%2C%22%ED%86%B5%EC%A0%9C%22%3A%22%22%2C%22%EC%9E%AC%EB%82%9C%22%3A%22%22%2C%22%EA%B8%B0%ED%83%80%22%3A%22%22%7D&incident_type=%7B%22%EC%82%AC%EA%B3%A0%22%3A%22%22%2C%22%EA%B3%B5%EC%82%AC%22%3A%22none%22%2C%22%ED%96%89%EC%82%AC%22%3A%22none%22%2C%22%EA%B8%B0%EC%83%81%22%3A%22none%22%2C%22%ED%86%B5%EC%A0%9C%22%3A%22none%22%2C%22%EC%9E%AC%EB%82%9C%22%3A%22none%22%2C%22%EA%B8%B0%ED%83%80%22%3A%22none%22%7D&hideDamagedRoad="
)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0"


# 헬퍼 함수: HTML 데이터를 받아옴
async def make_nws_request(url: str) -> str | None:
    logger.debug("URL 요청 시작: %s", url)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            logger.debug("응답 수신 완료: 상태 코드 %d", response.status_code)
            return response.text
        except Exception as e:
            logger.exception("URL 요청 중 오류 발생: %s", url)
            return None


# 도구 구현: HTML 결과에서 날짜와 사고 설명을 파싱
@mcp.tool()
async def get_alerts() -> str:
    logger.info("get_alerts 호출됨, state 인자: Seoul")
    url = f"{NWS_API_BASE}"
    logger.debug("사용할 URL: %s", url)
    html = await make_nws_request(url)

    if not html:
        logger.error("API에서 HTML 데이터를 받지 못함")
        return "경보를 가져올 수 없거나 경보가 없습니다."

    logger.debug("받은 HTML 길이: %d", len(html))
    soup = BeautifulSoup(html, 'html.parser')

    # ul 태그의 class가 "road_result_list02" 내의 li 요소 선택
    li_elements = soup.select("ul.road_result_list02 li")
    logger.debug("파싱된 알림 항목 개수: %d", len(li_elements))

    if not li_elements:
        logger.info("알림 항목이 없음")
        return "경보가 없습니다."

    results = []
    for index, li in enumerate(li_elements):
        # 날짜 정보 추출: <p class="date"> 태그
        p_date = li.find("p", class_="date")
        if p_date:
            a_tag = p_date.find("a")
            if a_tag:
                a_tag.extract()  # 링크 텍스트 제거
            date_text = p_date.get_text(strip=True)
        else:
            date_text = "날짜 정보 없음"
            logger.warning("항목 #%d: 날짜 정보 없음", index)

        # 사고 설명 추출: 두 번째 <p> 태그
        p_tags = li.find_all("p")
        if len(p_tags) >= 2:
            accident_text = p_tags[1].get_text(strip=True)
        else:
            accident_text = "내용 정보 없음"
            logger.warning("항목 #%d: 내용 정보 없음", index)

        result = f"날짜: {date_text}\n내용: {accident_text}"
        logger.debug("항목 #%d 파싱 결과: %s", index, result)
        results.append(result)

    final_result = "\n---\n".join(results)
    logger.info("최종 결과 준비 완료")
    return final_result


# 서버 실행 (이 예제에서는 STDIO 모드를 사용)
if __name__ == "__main__":
    # mcp.run(transport='stdio')
    mcp.run(transport='sse')
