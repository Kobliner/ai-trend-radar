import json
import os
import tweepy  # 트위터 연동 라이브러리

# 깃허브 시크릿에서 키 불러오기
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

def post_trend():
    # trends.json 파일 읽기
    try:
        with open("trends.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # 딕셔너리 구조에서 첫 번째 카테고리('dev')의 첫 번째 아이템 가져오기[cite: 2]
            first_category = list(data.keys())[0]
            latest_trend = data[first_category]["items"][0]
    except Exception as e:
        print(f"데이터를 읽지 못했습니다: {e}")
        return

    # 트윗 내용 구성 (프롬프트 내용 일부 포함)
    prompt_snippet = latest_trend.get('prompt', '')[:80] + "..."
    tweet_text = f"""🔥 오늘의 실시간 AI 트렌드 & 프롬프트

📌 주제: {latest_trend.get('title')}
💡 프롬프트 미리보기: {prompt_snippet}

👉 자세히 보기: https://ai-trend-radar-iota.vercel.app/
#AI #프롬프트 #챗GPT #개발자"""

    # 트위터 API 클라이언트 인증
    client = tweepy.Client(
        consumer_key=API_KEY, consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET
    )

    # 트윗 게시
    try:
        client.create_tweet(text=tweet_text)
        print("트위터 자동 포스팅 성공!")
    except Exception as e:
        print(f"포스팅 실패: {e}")

if __name__ == "__main__":
    post_trend()