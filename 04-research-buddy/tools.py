import re
import time

import httpx

HEADERS = {
    "User-Agent": (
        "ai-agent-learning/1.0 "
        "(https://github.com/oleeahmmed/agentic-ai-development; educational project)"
    )
}
API_URL = "https://en.wikipedia.org/w/api.php"

_PAGES = {}


def clean(text):
    return re.sub(r"<[^>]+>", "", text or "")


def get_json(params):
    for attempt in range(3):
        response = httpx.get(
            API_URL,
            params=params,
            headers=HEADERS,
            timeout=15,
            trust_env=False,
        )

        if response.status_code == 200:
            return response.json()

        time.sleep(1 + attempt)

    return {}


def search_wikipedia(query, limit=3):
    data = get_json(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": limit,
        }
    )
    results = data.get("query", {}).get("search", [])

    return [
        {
            "title": item["title"],
            "url": "https://en.wikipedia.org/wiki/" + item["title"].replace(" ", "_"),
            "snippet": clean(item.get("snippet", "")),
        }
        for item in results
    ]


def read_page(title):
    if title in _PAGES:
        return _PAGES[title]

    data = get_json(
        {
            "action": "query",
            "prop": "extracts",
            "explaintext": 1,
            "redirects": 1,
            "titles": title,
            "format": "json",
            "utf8": 1,
        }
    )
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), None)

    if not page or "missing" in page:
        _PAGES[title] = None
        return None

    result = {
        "title": page.get("title", title),
        "url": "https://en.wikipedia.org/wiki/" + page.get("title", title).replace(" ", "_"),
        "text": page.get("extract", ""),
    }

    _PAGES[title] = result

    return result


def search_and_read(query, limit=2):
    pages = []

    for result in search_wikipedia(query, limit):
        time.sleep(0.5)
        page = read_page(result["title"])

        if page and page["text"]:
            pages.append(page)

    return pages
