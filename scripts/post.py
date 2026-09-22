import os
import tweepy  # 트위터 연동 라이브러리

# 깃허브 시크릿에서 키 불러오기
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

def post_trend():
    # trends.json 파일을 읽는 대신 직접 최신 트렌드 탑 1위를 정의합니다.
    latest_title = "LLM 기반 코드 리팩토링 및 성능 최적화"
    latest_prompt = "다음 [언어] 코드를 분석하여 시간 복잡도와 공간 복잡도를 최적화해줘."

    # 트윗 내용 구성
    tweet_text = f"""🔥 오늘의 실시간 AI 트렌드 & 프롬프트

📌 주제: {latest_title}
💡 프롬프트 미리보기: {latest_prompt}

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