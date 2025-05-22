print("✅ Flask 앱 시작됨")

from flask import Flask
from news_alert import run_news_once

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Flask 작동 확인</title>
    </head>
    <body>
        <h1>🌐 Flask 서버 정상 작동!</h1>
        <p>✅ Render 배포 성공, Flask 서버가 응답하고 있습니다.</p>
        <p><a href="/run">/run → 뉴스 전송 테스트</a></p>
    </body>
    </html>
    """

@app.route("/run")
def run_news():
    try:
        counter = 1
        run_news_once(counter)
        return "📢 뉴스 전송 완료!"
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}", 500

# gunicorn용 app 객체는 여기서 인식됨
