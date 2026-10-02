from __future__ import annotations

import json
import re
from typing import Any

import requests


def build_llm_config() -> dict[str, Any]:
    return {
        "model": "mistral",
        "api_key": "unused",
        "base_url": "http://localhost:1234/v1",
        "api_type": "open_ai",
        "temperature": 0.2,
    }


def get_local_completion(prompt: str, model: str = "mistral") -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return ""


def score_job_against_cv(job: dict[str, Any], cv_text: str) -> dict[str, Any]:
    job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('company', '')}".lower()
    cv_lower = cv_text.lower()

    required_keywords = [
        "python",
        "sql",
        "api",
        "backend",
        "docker",
        "aws",
        "fastapi",
        "django",
        "microservices",
        "cloud",
    ]

    found = [kw for kw in required_keywords if kw in job_text and kw in cv_lower]
    missing = [kw for kw in required_keywords if kw in job_text and kw not in cv_lower]

    score = min(100, max(30, round((len(found) / max(len(required_keywords), 1)) * 100)))

    if not found:
        score = 35

    summary = (
        f"Strong fit for {job.get('title', 'role')} because the profile includes {', '.join(found[:3]) or 'core technical context'}."
        if found
        else f"Moderate fit for {job.get('title', 'role')}; the profile is not yet aligned with the most relevant keywords."
    )

    return {
        "match_score": score,
        "fit_summary": summary,
        "missing_skills": ", ".join(missing[:5]) if missing else "No major gaps detected",
        "action": "Apply now"
        if score >= 70
        else "Review and tailor CV"
        if score >= 50
        else "Skip for now",
    }


def build_daily_digest(scored_jobs: list[dict[str, Any]]) -> str:
    sorted_jobs = sorted(scored_jobs, key=lambda item: item["match_score"], reverse=True)
    top = sorted_jobs[:3]
    medium = [item for item in sorted_jobs if 50 <= item["match_score"] < 70]

    lines = [
        "# Daily job digest",
        f"- Strong matches: {len(top)}",
        f"- Medium matches: {len(medium)}",
        "",
        "## Best targets",
    ]

    for item in top:
        lines.append(f"- {item['title']} @ {item['company']} ({item['match_score']}% fit) -> {item['action']}")

    lines.extend(["", "## Actions to take", "- Tailor the CV to the top 3 roles.", "- Prepare a short intro for the best opportunities.", "- Follow up on pending applications."])
    return "\n".join(lines)
