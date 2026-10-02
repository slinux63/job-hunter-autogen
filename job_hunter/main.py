from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from job_hunter.agents import build_daily_digest, score_job_against_cv
from job_hunter.config import get_settings
from job_hunter.db import JobStore
from job_hunter.sources import fetch_public_jobs


def load_cv(path: str) -> str:
    file_path = Path(path)
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return """# Default Profile Summary

## Core Skills
- Python, FastAPI, Django, SQL, PostgreSQL
- REST APIs, microservices architecture
- Docker, Kubernetes, AWS, CI/CD
- Backend development, system design
"""


def create_sample_cv(path: str) -> None:
    file_path = Path(path)
    if file_path.exists():
        return
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        """# Candidate profile

## Summary
Python backend developer with experience in APIs, SQL, Docker, cloud deployment, and system design.

## Skills
- Python
- FastAPI
- Django
- SQL / PostgreSQL
- REST APIs
- Docker
- AWS
- CI/CD
- Microservices

## Experience
- Built internal API services and data workflows
- Improved deployment reliability with Docker and CI pipelines
- Worked on service integration and observability

## Goals
Looking for backend engineering roles focused on Python, API products, and scalable systems.
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local AI job hunter")
    parser.add_argument("--keywords", default=None, help="Job keywords")
    parser.add_argument("--location", default=None, help="Search location")
    parser.add_argument("--limit", type=int, default=None, help="Maximum jobs")
    parser.add_argument("--output", default="data/daily_digest.md", help="Digest output path")
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

    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    create_sample_cv(settings.cv_path)

    store = JobStore(settings.db_path)
    jobs = fetch_public_jobs(settings.job_keywords, settings.job_location, limit=settings.max_results)
    store.save_offers(jobs)

    cv_text = load_cv(settings.cv_path)
    scored_jobs = []
    for job in jobs:
        result = score_job_against_cv(job, cv_text)
        scored = {**job, **result}
        scored_jobs.append(scored)
        store.save_application(job, result["match_score"], result["fit_summary"], result["missing_skills"], result["action"])

    digest = build_daily_digest(scored_jobs)
    store.save_summary(digest)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(digest, encoding="utf-8")
    store.close()

    print(json.dumps({"timestamp": datetime.now().isoformat(), "jobs": scored_jobs, "digest": digest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
