import requests
import feedparser
import html

# 주요 키워드 목록
KEYWORDS = [
    "그라시움", "보험개발원", "보험정비협의회", "복원수리", "삼성손사", "삼성화재교통안전문화연구소",
    "수리비", "아르테온", "아우다텍스", "와산차부품", "인트라밴", "자동차관리법", "자배법",
    "정비연합회", "정비요금", "표준작업시간", "허창언", "AOS2017", "AOS알파", "audatex",
    "hhajun@kidi.or.kr", "hhajun@naver.com", "repair cost", "thatcham"
]

def run_news_once():
    result = []

    for keyword in KEYWORDS:
        feed_url = f"https://news.google.com/rss/search?q={requests.utils.quote(keyword)}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(feed_url)

        items = []
        for entry in feed.entries:
            if keyword.lower() in entry.title.lower() or keyword.lower() in entry.summary.lower():
                title = html.escape(entry.title)
                link = entry.link
                items.append(f'📎 <a href="{link}">{title}</a>')
                if len(items) >= 7:
                    break

        if items:
            news_block = f"<b>📌 키워드: {keyword}</b>\n" + "\n".join(items)
            result.append(news_block)

    return "<br><br>".join(result) if result else "🔍 최근 뉴스 없음."
