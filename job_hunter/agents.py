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
    loc = location.strip().replace(" ", ")
    return [url.format(query=q, location=loc) for url in DEFAULT_SEARCH_URLS]


def fetch_public_jobs(query: str, location: str, limit: int = 10) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in search_urls(query, location):
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select("a, .job_seen_beacon, .job-card, .job-card-container")[:limit]

        for card in cards:
            title = normalize_text(card.get_text(" ", strip=True))
            if not title:
                continue
            jobs.append(
                {
                    "source": "public_search",
                    "title": title[:120],
                    "company": "Public source",
                    "location": location,
                    "url": url,
                    "salary": "N/A",
                    "description": "Fetched from public search page",
                }
            )
            if len(jobs) >= limit:
                return jobs

    if not jobs:
        jobs.append(
            {
                "source": "demo",
                "title": "Example job: Python backend developer",
                "company": "Example Company",
                "location": location,
                "url": "https://example.com/job",
                "salary": "€60-90k",
                "description": "Demo record used when no public sources are reachable.",
            }
        )
    return jobs[:limit]
