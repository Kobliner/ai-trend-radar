import os
import tweepy

def post_trend():
    print("트위터 포스팅 스크립트 실행 시작...")

    API_KEY = os.environ.get("TWITTER_API_KEY")
    API_SECRET = os.environ.get("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        print("에러: 깃허브 시크릿 키가 설정되지 않았습니다!")
        return

    tweet_text = """🔥 오늘의 실시간 AI 트렌드 & 프롬프트

📌 주제: LLM 기반 코드 리팩토링 및 성능 최적화
💡 프롬프트 미리보기: 다음 코드를 분석하여 시간/공간 복잡도를 최적화해줘.

👉 자세히 보기: https://ai-trend-radar-iota.vercel.app/
#AI #프롬프트 #챗GPT #개발자"""

    try:
        client = tweepy.Client(
            consumer_key=API_KEY, 
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN, 
            access_token_secret=ACCESS_SECRET
        )
        
        response = client.create_tweet(text=tweet_text)
        print(f"트위터 자동 포스팅 성공! 응답: {response}")
    except Exception as e:
        print(f"트위터 API 전송 중 에러 발생: {e}")

if __name__ == "__main__":
    post_trend()
