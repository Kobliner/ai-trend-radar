import json
import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable is missing!")
    exit(1)

# 구글 Gemini 클라이언트 초기화
client = genai.Client(api_key=api_key)

prompt_template = """
당신은 최고의 AI 트렌드 분석가입니다. 
다음 6개 카테고리(개발 & 코드, 비즈니스 & 문서, 콘텐츠 기획, 스포츠, 게임, 일상) 각각에 대해, 
현재 시점에서 가장 주목받는 최신 AI 활용 주제와 실무에서 바로 쓸 수 있는 프롬프트 5개씩을 JSON 포맷으로 생성해주세요.

반드시 아래의 JSON 구조를 정확히 지켜주세요. 마크다운 백틱(```json 등) 없이 순수 JSON 문자열만 반환해야 합니다.

{
  "dev": {
    "title": "개발 & 코드 트렌드",
    "items": [
      { "rank": 1, "count": "1.2k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "950 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "820 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "670 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "540 신호", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "business": {
    "title": "비즈니스 & 문서 트렌드",
    "items": [
      { "rank": 1, "count": "980 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "840 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "710 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "620 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "510 신호", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "creative": {
    "title": "콘텐츠 기획 트렌드",
    "items": [
      { "rank": 1, "count": "1.5k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "1.1k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "890 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "760 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "640 신호", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "sports": {
    "title": "스포츠 트렌드",
    "items": [
      { "rank": 1, "count": "850 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "720 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "610 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "530 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "420 신호", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "game": {
    "title": "게임 트렌드",
    "items": [
      { "rank": 1, "count": "1.1k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "940 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "810 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "690 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "550 신호", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "daily": {
    "title": "일상 트렌드",
    "items": [
      { "rank": 1, "count": "2.3k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "1.8k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "1.4k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "1.1k 신호", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "920 신호", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  }
}
"""

try:
    print("Calling Gemini API to generate trends...")
    # 무료로 사용 가능한 Gemini Flash 모델 호출
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_template,
    )
    
    content = response.text.strip()
    
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    parsed_data = json.loads(content)

    with open("trends.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)

    print("Successfully updated trends.json using Gemini!")

except Exception as e:
    print(f"Error generating trends: {type(e).__name__} - {e}")
    exit(1)