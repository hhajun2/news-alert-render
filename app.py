from flask import Flask
from news_alert import run_news_once

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ 뉴스 알림 시스템이 정상 작동 중입니다."

@app.route("/run")
def run_news():
    try:
        counter = 1
        run_news_once(counter)
        return "✅ 뉴스 전송 완료!"
    except Exception as e:
        return f"❌ 오류 발생: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
