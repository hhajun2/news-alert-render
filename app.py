from flask import Flask
from news_alert import run_news_once

app = Flask(__name__)

@app.route("/")
def index():
    return "📢 뉴스 알림 봇 실행 중입니다."

@app.route("/run")
def run_news():
    try:
        counter = 1  # 더미 값
        run_news_once()
        return "✅ 뉴스 전송 완료"
    except Exception as e:
        return f"❌ 오류 발생: {e}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render가 자동 지정하는 포트
    app.run(host="0.0.0.0", port=port)         # 고정값 10000 ❌, 반드시 환경변수 사용
