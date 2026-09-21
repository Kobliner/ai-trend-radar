import json
import os
from openai import OpenAI

# 1. OpenAI 클라이언트 초기화 (GitHub Secrets에서 가져올 예정)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
      ... (총 5개)
    ]
  },
  "business": { ... },
  "creative": { ... },
  "sports": { ... },
  "game": { ... },
  "daily": { ... }
}
"""

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 빠르고 정확한 모델 사용
        messages=[{"role": "user", "content": prompt_template}],
        temperature=0.7,
    )
    
    content = response.choices[0].message.content.strip()
    
    # 혹시 모를 마크다운 태그 제거
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    # JSON 파싱 검증
    parsed_data = json.loads(content)

    # trends.json 파일로 저장
    with open("trends.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)

    print("Successfully updated trends.json!")

except Exception as e:
    print(f"Error generating trends: {e}")
    exit(1)