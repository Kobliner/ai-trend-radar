import os
import json
from google import genai

# 1. Gemini 클라이언트 초기화 (본인의 API 키를 입력하거나 환경변수 사용)
client = genai.Client(api_key=os.environ.get('GCP_API_KEY'))

def generate_ai_trends():
    print("🔄 AI 인기 질문 순위를 생성하는 중...")

    # 2. 프롬프트 작성 (JSON 형식으로만 출력하도록 지시)
    prompt = """
    너는 'AI Trend Radar' 서비스의 데이터 에디터야. 
    현재 가장 핫한 기술, 개발, 비즈니스, 콘텐츠 트렌드를 반영하여,
    사람들이 AI(챗GPT, 제미나이 등)에게 가장 많이 물어볼 만한 실무/인기 질문 순위 데이터를 아래의 JSON 형식으로만 정확히 만들어줘.
    
    다른 설명이나 텍스트는 절대 포함하지 말고, 순수한 JSON 코드 블록만 출력해줘.

    [JSON 구조]
    {
      "dev": {
        "title": "🔥 개발 & 코드 분야 실시간 인기 질문 순위",
        "items": [
          {"rank": 1, "title": "React 컴포넌트 리렌더링 최적화", "count": "조회 급상승", "prompt": "다음 React 코드에서 불필요한 리렌더링이 발생하는 원인을 찾고, 최적화된 코드를 작성해줘."},
          {"rank": 2, "title": "Python FastAPI 비동기 처리 구조", "count": "안정적", "prompt": "FastAPI에서 외부 API를 병렬로 호출하기 위한 비동기 패턴 사용법을 예시와 함께 설명해줘."},
          {"rank": 3, "title": "SQL 쿼리 성능 튜닝 및 인덱스 설계", "count": "관심 집중", "prompt": "대용량 테이블 조인 쿼리의 속도를 개선하기 위한 인덱스 설계 방안을 제안해줘."}
        ]
      },
      "business": {
        "title": "📈 비즈니스 & 문서 분야 실시간 인기 질문 순위",
        "items": [
          {"rank": 1, "title": "신사업 기획서 초안 프레임워크 구조", "count": "조회 급상승", "prompt": "B2B SaaS 서비스를 위한 기획서 목차와 핵심 내용을 짜줘."},
          {"rank": 2, "title": "분기별 실적 보고서 요약 및 인사이트", "count": "안정적", "prompt": "분기별 매출 데이터를 바탕으로 경영진 보고용 핵심 요약과 리스크를 분석해줘."},
          {"rank": 3, "title": "영문 비즈니스 이메일 톤 교정", "count": "꾸준한 인기", "prompt": "파트너사 발송용 영문 이메일 초안을 원어민 비즈니스 톤에 맞게 수정해줘."}
        ]
      },
      "creative": {
        "title": "🎨 콘텐츠 기획 분야 실시간 인기 질문 순위",
        "items": [
          {"rank": 1, "title": "유튜브 숏폼 대본 3초 후크 구성", "count": "조회 급상승", "prompt": "유튜브 쇼츠 초반 3초 안에 시청자의 이탈을 막을 수 있는 강력한 후크 문구를 제안해줘."},
          {"rank": 2, "title": "블로그 SEO 최적화 아웃라인 작성", "count": "안정적", "prompt": "구글 검색 상위 노출을 위한 H2, H3 태그 구조의 블로그 포스팅 아웃라인을 짜줘."},
          {"rank": 3, "title": "인스타그램 카드뉴스 스토리보드", "count": "관심 집중", "prompt": "인스타그램 카드뉴스 5장 분량의 이미지 문구와 핵심 내용을 구성해줘."}
        ]
      }
    }
    """

    # 3. Gemini 모델 호출 (안정적인 gemini-3.6-flash 사용)
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )

    # 4. 결과 확인 및 파일 저장
    result_text = response.text.strip()
    
    # 마크다운 코드 블록 제거
    if result_text.startswith("```json"):
        result_text = result_text[7:]
    if result_text.endswith("```"):
        result_text = result_text[:-3]
    
    result_text = result_text.strip()

    # JSON 파일로 저장
    with open("trends.json", "w", encoding="utf-8") as f:
        f.write(result_text)

    print("✔ 트렌드 데이터 생성 완료! 'trends.json' 파일이 저장되었습니다.")
    print(result_text)

if __name__ == "__main__":
    generate_ai_trends()
