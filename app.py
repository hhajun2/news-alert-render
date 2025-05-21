from flask import Flask
import requests, feedparser, html
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from urllib.parse import quote
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

keywords = [
    '그라시움', '보험개발원', '보험정비협의회', '복원수리', '삼성손사',
    '삼성화재교통안전문화연구소', '수리비', '아르테온', '아우다텍스',
    '와산차부품', '인트라밴', '자동차관리법', '자배법', '정비연합회',
    '정비요금', '표준작업시간', '허창언', 'AOS2017', 'AOS알파',
    'audatex', 'hhajun@kidi.or.kr', 'hhajun@naver.com',
    'repair cost', 'thatcham'
]

def remove_similar_titles(articles, threshold=0.85):
    unique = []
    for title, link in articles:
        if not any(SequenceMatcher(None, title, t).ratio() > threshold for t, _ in unique):
            unique.append((title, link))
    return unique

def search_google_news(keyword):
    encoded_kw = quote(keyword + ' when:3h')
    url = f'https://news.google.com/rss/search?q={encoded_kw}&hl=ko&gl=KR&ceid=KR:ko'
    feed = feedparser.parse(url)
    raw = [(entry.title, entry.link) for entry in feed.entries[:10]]
    raw = remove_similar_titles(raw)
    return [(html.escape(title), link) for title, link in raw[:7]]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)

@app.route("/run", methods=["GET"])
def run_news_alert():
    now_kst = datetime.utcnow() + timedelta(hours=9)
    send_telegram(f"🗞️ {now_kst.strftime('%Y-%m-%d %H:%M')} (KST) 기준 뉴스 요약")

    for kw in keywords:
        articles = search_google_news(kw)
        if articles:
            body = f"\n📌 키워드: {html.escape(kw)}\n" + "\n\n".join(
                f'<a href="{link}">📎 {title}</a>' for title, link in articles
            )
            send_telegram(body)
    return "✅ 뉴스 전송 완료", 200

@app.route("/")
def home():
    return "🔔 뉴스 알림 봇 실행 중입니다.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
