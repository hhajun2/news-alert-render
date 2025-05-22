print("✅ Flask 앱 시작됨")


from flask import Flask
from news_alert import run_news_once

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>🌐 Flask 서버 정상 작동!</h1>"

@app.route("/run")
def run_news():
    try:
        counter = 1
        run_news_once(counter)
        return "📢 뉴스 전송 완료!"
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}", 500

# gunicorn용 app 객체는 여기서 인식됨

