from __future__ import annotations

import argparse
import json
from pathlib import Path

from job_hunter.agents import build_daily_digest, score_job_against_cv
from job_hunter.config import ensure_dirs, get_settings
from job_hunter.db import JobStore
from job_hunter.sources import fetch_public_jobs


def load_cv(path: str) -> str:
    file_path = Path(path)
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return """Profile summary:
Python backend developer with API, SQL, Docker, and cloud experience.
Core skills: Python, FastAPI, PostgreSQL, microservices, CI/CD, system design.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local AI job hunter")
    parser.add_argument("--keywords", default=None, help="Job keywords, e.g. python backend")
    parser.add_argument("--location", default=None, help="Search location, e.g. Paris")
    parser.add_argument("--limit", type=int, default=10, help="Maximum jobs to evaluate")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    if args.keywords:
        settings.job_keywords = args.keywords
    if args.location:
        settings.job_location = args.location
    if args.limit:
        settings.max_results = args.limit

    ensure_dirs()
    store = JobStore(settings.db_path)

    jobs = fetch_public_jobs(settings.job_keywords, settings.job_location, limit=settings.max_results)
    store.save_offers(jobs)

    cv_text = load_cv(settings.cv_path)
    scored_jobs = []
    for job in jobs:
        result = score_job_against_cv(job, cv_text)
        scored_jobs.append({
            **job,
            "match_score": result["match_score"],
            "fit_summary": result["fit_summary"],
            "missing_skills": result["missing_skills"],
            "action": result["action"],
        })
        store.save_application(job, result["match_score"], result["fit_summary"], result["missing_skills"], result["action"])

    digest = build_daily_digest(scored_jobs)
    store.save_summary(digest)
    store.close()

    print(json.dumps({
        "jobs": scored_jobs,
        "digest": digest,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
