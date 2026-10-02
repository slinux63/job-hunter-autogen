from __future__ import annotations

import re
from typing import Any

import requests
from bs4 import BeautifulSoup

DEFAULT_SEARCH_URLS = [
    "https://www.indeed.com/jobs?q={query}&l={location}",
    "https://www.welcometothejungle.com/fr/jobs?query={query}&location={location}",
]


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def search_urls(query: str, location: str) -> list[str]:
    q = query.strip().replace(" ", "+")
    loc = location.strip().replace(" ", "+")
    return [url.format(query=q, location=loc) for url in DEFAULT_SEARCH_URLS]


def fetch_public_jobs(query: str, location: str, limit: int = 10) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for url in search_urls(query, location):
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select("a, [class*='job'], [class*='card']")[:limit]

        for card in cards:
            title = normalize_text(card.get_text(" ", strip=True))
            if not title or len(title) < 10:
                continue
            jobs.append({
                "source": "public_search",
                "title": title[:150],
                "company": "Public source",
                "location": location,
                "url": url,
                "salary": "N/A",
                "description": f"Fetched from public search page: {query}",
            })
            if len(jobs) >= limit:
                return jobs

    if not jobs:
        jobs.extend([
            {
                "source": "demo",
                "title": "Python Backend Developer",
                "company": "Tech Startup",
                "location": location,
                "url": "https://example.com/job/1",
                "salary": "€60-80k",
                "description": "Build scalable APIs with Python, FastAPI, PostgreSQL. Docker & AWS experience required.",
            },
            {
                "source": "demo",
                "title": "Senior Backend Engineer",
                "company": "Enterprise Solutions",
                "location": location,
                "url": "https://example.com/job/2",
                "salary": "€80-120k",
                "description": "Lead backend architecture for microservices. Python, Kubernetes, CI/CD pipeline expertise.",
            },
        ])

    return jobs[:limit]
