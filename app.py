from flask import Flask
from news_alert import run_news_once

app = Flask(__name__)

@app.route("/")
def index():
    return "🔔 뉴스 알림 봇 실행 중입니다."

@app.route("/run")
def run_news():
    try:
        counter = 1  # 초기 counter 값
        run_news_once(counter)
        return "✅ 뉴스 전송 완료"
    except Exception as e:
        return f"❌ 오류 발생: {e}"
