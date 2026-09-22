import json
import os
import time
from datetime import datetime
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable is missing!")
    exit(1)

client = genai.Client(api_key=api_key)

prompt_template = """
당신은 최고의 AI 트렌드 분석가입니다. 
다음 6개 카테고리(개발 & 코드, 비즈니스 & 문서, 콘텐츠 기획, 스포츠, 게임, 일상) 각각에 대해, 
현재 시점에서 가장 주목받는 최신 AI 활용 주제와 실무에서 바로 쓸 수 있는 프롬프트 5개씩을 JSON 포맷으로 생성해주세요.

**중요 규칙:**
1. 각 아이템의 `count` 값(예: "1.2k 트렌드", "850 트렌드" 등)은 고정하지 말고, 매번 400부터 3,000 사이의 임의의 트래픽/반응 수치를 자연스럽고 다채롭게(예: '1.5k 트렌드', '920 트렌드', '2.1k 트렌드' 등) 생성해주세요.
2. 반드시 아래의 JSON 구조를 정확히 지켜주세요. 마크다운 백틱(```json 등) 없이 순수 JSON 문자열만 반환해야 합니다.

{
  "dev": {
    "title": "개발 & 코드 트렌드",
    "items": [
      { "rank": 1, "count": "1.2k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "950 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "820 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "670 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "540 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "business": {
    "title": "비즈니스 & 문서 트렌드",
    "items": [
      { "rank": 1, "count": "980 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "840 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "710 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "620 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "510 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "creative": {
    "title": "콘텐츠 기획 트렌드",
    "items": [
      { "rank": 1, "count": "1.5k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "1.1k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "890 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "760 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "640 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "sports": {
    "title": "스포츠 트렌드",
    "items": [
      { "rank": 1, "count": "850 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "720 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "610 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "530 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "420 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "game": {
    "title": "게임 트렌드",
    "items": [
      { "rank": 1, "count": "1.1k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "940 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "810 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "690 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "550 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  },
  "daily": {
    "title": "일상 트렌드",
    "items": [
      { "rank": 1, "count": "2.3k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 2, "count": "1.8k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 3, "count": "1.4k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 4, "count": "1.1k 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" },
      { "rank": 5, "count": "920 트렌드", "title": "주제 제목", "prompt": "프롬프트 내용" }
    ]
  }
}
"""

max_retries = 3
success = False

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1}: Calling Gemini API...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
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

        # 1. trends.json 최신화 저장
        with open("trends.json", "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        # 2. history.json 에 아카이브 기록 누적
        history_file = "history.json"
        history_data = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as hf:
                    history_data = json.load(hf)
            except:
                history_data = []

        current_time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M (UTC)")
        
        snapshot = {
            "timestamp": current_time_str,
            "keywords": { 
                cat: [item["title"] for item in data.get("items", [])] 
                for cat, data in parsed_data.items() 
            }
        }

        history_data.insert(0, snapshot)
        history_data = history_data[:50]

        with open(history_file, "w", encoding="utf-8") as hf:
            json.dump(history_data, hf, ensure_ascii=False, indent=2)

        print("Successfully updated trends.json and archived to history.json!")
        success = True
        break

    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {type(e).__name__} - {e}")
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 10
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        else:
            print("All retry attempts failed.")
            exit(1)