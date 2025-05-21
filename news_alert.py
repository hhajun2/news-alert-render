import requests, feedparser, html, json, re
from datetime import datetime, timedelta
from konlpy.tag import Okt
from difflib import SequenceMatcher
from urllib.parse import quote

# 텔레그램 설정
BOT_TOKEN = '8197776941:AAHB__lnAwtYMNYZoc0tH97-HwriIGkKzkQ'
CHAT_ID = 6881404336

keywords = [
    '그라시움', '보험개발원', '보험정비협의회', '복원수리', '삼성손사',
    '삼성화재교통안전문화연구소', '수리비', '아르테온', '아우다텍스',
    '와산차부품', '인트라밴', '자동차관리법', '자배법', '정비연합회',
    '정비요금', '표준작업시간', '허창언', 'AOS2017', 'AOS알파',
    'audatex', 'hhajun@kidi.or.kr', 'hhajun@naver.com',
    'repair cost', 'thatcham'
]

okt = Okt()

def is_within_active_hours():
    now_kst = datetime.utcnow() + timedelta(hours=9)
    return 7 <= now_kst.hour < 22

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
    print(f"🔎 '{keyword}' → {len(feed.entries)}개")
    raw = [(entry.title, entry.link) for entry in feed.entries[:10]]
    raw = remove_similar_titles(raw)
    raw = raw[:7]
    return [(html.escape(title), link) for title, link in raw]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    res = requests.post(url, data=payload)
    print(f"[전송 상태] {res.status_code}")
    if res.status_code != 200:
        print("🧾 실패:", message[:300])

def run_news_alert():
    if not is_within_active_hours():
        print("⏸️ 운영시간 아님. 종료")
        return

    now_kst = datetime.utcnow() + timedelta(hours=9)
    header = f"🗞️ {now_kst.strftime('%Y-%m-%d %H:%M')} (KST) 기준 뉴스 요약"
    send_telegram(header)

    for kw in keywords:
        articles = search_google_news(kw)
        if articles:
            body = f"\n📌 키워드: {html.escape(kw)}\n" + "\n\n".join(
                f'<a href="{link}">📎 {title}</a>' for title, link in articles
            )
            send_telegram(body)

# 실행
if __name__ == '__main__':
    run_news_alert()
