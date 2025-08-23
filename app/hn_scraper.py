from typing import List
import httpx
from bs4 import BeautifulSoup
from cachetools import TTLCache
from .models import HNEntry

_HN_URL = "https://news.ycombinator.com/"
_cache = TTLCache(maxsize=1, ttl=120)  # 2 min caché


async def fetch_html() -> str:
    headers = {"User-Agent": "hn-scraper-fastapi/1.0"}
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(headers=headers, timeout=timeout) as client:
        r = await client.get(_HN_URL)
        r.raise_for_status()
        return r.text


async def scrape_first_30() -> List[HNEntry]:
    if "entries" in _cache:
        return _cache["entries"]

    html = await fetch_html()
    soup = BeautifulSoup(html, "lxml")

    entries: List[HNEntry] = []
    for athing in soup.select("tr.athing"):
        # rank
        rank_el = athing.select_one("span.rank")
        rank = int(rank_el.get_text(strip=True).replace(".", "")) if rank_el else 0

        # title
        title_a = athing.select_one("span.titleline > a") or athing.select_one(
            "a.storylink"
        )
        title = title_a.get_text(strip=True) if title_a else ""

        # subtext (fila siguiente)
        sub = athing.find_next_sibling("tr")
        points = 0
        comments = 0
        if sub:
            score_el = sub.select_one("span.score")  # <-- fix aquí
            if score_el:
                try:
                    points = int(score_el.get_text(strip=True).split()[0])
                except Exception:
                    points = 0

            # último enlace con "comment" o "discuss"
            for a in reversed(sub.select("a")):
                txt = (a.get_text(strip=True) or "").lower()
                if txt.startswith("discuss"):
                    comments = 0
                    break
                if "comment" in txt:
                    num = "".join(ch for ch in txt if ch.isdigit())
                    comments = int(num) if num else 0
                    break

        entries.append(
            HNEntry(rank=rank, title=title, points=points, comments=comments)
        )
        if len(entries) >= 30:
            break

    entries.sort(key=lambda e: e.rank)
    _cache["entries"] = entries
    return entries
