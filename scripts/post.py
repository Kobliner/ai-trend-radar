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
            latest_trend = data[0]  # 가장 최신 트렌드 선택
    except Exception as e:
        print(f"데이터를 읽지 못했습니다: {e}")
        return

    # 트윗 내용 구성
    tweet_text = f"""🔥 오늘의 실시간 AI 트렌드 & 프롬프트

📌 주제: {latest_trend.get('title')}
💡 {latest_trend.get('summary', '실무에서 유용한 AI 프롬프트를 확인하세요!')}

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