import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def fetch_github_trending() -> list[dict]:
    """Парсит трендовые репозитории GitHub за сегодня."""
    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as client:
        r = await client.get("https://github.com/trending?since=daily")
        r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    for row in soup.select("article.Box-row")[:15]:
        h2 = row.select_one("h2 a")
        if not h2:
            continue
        repo_path = h2.get("href", "").strip("/")
        desc = row.select_one("p")
        lang = row.select_one("[itemprop=programmingLanguage]")
        stars_today = row.select_one("span.d-inline-block.float-sm-right")

        items.append({
            "repo": repo_path,
            "url": f"https://github.com/{repo_path}",
            "description": desc.get_text(strip=True) if desc else "",
            "language": lang.get_text(strip=True) if lang else "—",
            "stars_today": stars_today.get_text(strip=True) if stars_today else "",
        })
    return items


async def fetch_hackernews_top() -> list[dict]:
    """Топ-20 постов Hacker News через официальный API."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        ids = r.json()[:20]

        tasks = [client.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json")
                 for i in ids]
        responses = await asyncio.gather(*tasks)

    items = []
    for resp in responses:
        data = resp.json()
        if not data or data.get("type") != "story":
            continue
        items.append({
            "title": data.get("title"),
            "url": data.get("url") or f"https://news.ycombinator.com/item?id={data['id']}",
            "score": data.get("score", 0),
            "comments": data.get("descendants", 0),
            "by": data.get("by"),
            "hn_url": f"https://news.ycombinator.com/item?id={data['id']}",
        })
    return items


async def fetch_habr_top() -> list[dict]:
    """Топ статьи Хабра за день."""
    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as client:
        r = await client.get("https://habr.com/ru/hub/development/articles/top/daily/")
        if r.status_code != 200:
            # fallback на главную
            r = await client.get("https://habr.com/ru/all/")

    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    for article in soup.select("article.tm-articles-list__item")[:10]:
        title_el = article.select_one("a.tm-title__link")
        href = article.select_one("a.tm-title__link")
        snippet = article.select_one("div.article-formatted-body")
        stats = article.select_one("span.tm-icon-star")

        if not title_el:
            continue
        link = href.get("href", "")
        if link.startswith("/"):
            link = "https://habr.com" + link

        items.append({
            "title": title_el.get_text(strip=True),
            "url": link,
            "snippet": snippet.get_text(" ", strip=True)[:200] if snippet else "",
            "rating": stats.parent.get_text(strip=True) if stats else "",
        })
    return items


async def collect_all() -> dict:
    """Собирает данные из всех источников параллельно."""
    gh, hn, habr = await asyncio.gather(
        fetch_github_trending(),
        fetch_hackernews_top(),
        fetch_habr_top(),
        return_exceptions=True,
    )
    return {
        "github": gh if isinstance(gh, list) else [],
        "hackernews": hn if isinstance(hn, list) else [],
        "habr": habr if isinstance(habr, list) else [],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }