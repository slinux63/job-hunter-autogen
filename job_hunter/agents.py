from __future__ import annotations

from typing import Any


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
        "kubernetes",
        "postgresql",
        "rest",
        "devops",
    ]

    found = [kw for kw in required_keywords if kw in job_text and kw in cv_lower]
    missing = [kw for kw in required_keywords if kw in job_text and kw not in cv_lower]

    if found:
        score = min(100, max(30, round((len(found) / max(len(required_keywords), 1)) * 100)))
    else:
        score = 35

    summary = f"Strong fit: profile includes {', '.join(found[:3])}." if found else "Moderate fit: profile lacks some key technical requirements."
    if score >= 75:
        action = "🎯 Apply immediately"
    elif score >= 60:
        action = "✅ Tailor CV and apply"
    elif score >= 45:
        action = "⚠️ Review and consider"
    else:
        action = "❌ Skip for now"

    return {
        "match_score": score,
        "fit_summary": summary,
        "missing_skills": ", ".join(missing[:5]) if missing else "No major gaps detected",
        "action": action,
    }


def build_daily_digest(scored_jobs: list[dict[str, Any]]) -> str:
    if not scored_jobs:
        return "# Daily Job Digest\n\nNo jobs found today.\n"

    sorted_jobs = sorted(scored_jobs, key=lambda item: item["match_score"], reverse=True)
    top = sorted_jobs[:3]
    medium = [item for item in sorted_jobs if 50 <= item["match_score"] < 75]
    low = [item for item in sorted_jobs if item["match_score"] < 50]

    lines = [
        "# 📋 Daily Job Digest",
        "**Today's summary:**",
        f"- 🎯 Strong matches: {len(top)}",
        f"- ✅ Medium matches: {len(medium)}",
        f"- ⚠️ Other opportunities: {len(low)}",
        f"- 📊 Total analyzed: {len(scored_jobs)}",
        "",
    ]

    if top:
        lines.extend(["## 🎯 Top Opportunities (Apply Now)", ""])
        for i, item in enumerate(top, 1):
            lines.append(
                f"{i}. **{item['title']}** @ {item['company']} | {item['location']}\n"
                f"   - Match: {item['match_score']}% | {item['fit_summary']}\n"
                f"   - Action: {item['action']}\n"
            )

    if medium:
        lines.extend(["## ✅ Worth Reviewing (Tailor & Apply)", ""])
        for i, item in enumerate(medium[:3], 1):
            lines.append(
                f"{i}. **{item['title']}** @ {item['company']} | {item['location']}\n"
                f"   - Match: {item['match_score']}% | {item['fit_summary']}\n"
            )

    lines.extend([
        "",
        "## 📌 Next Steps",
        "1. Review the top 3 opportunities in detail",
        "2. Tailor your CV and cover letter for each",
        "3. Personalize your outreach message",
        "4. Track applications and follow-ups",
        "5. Update your CV with new skills as you learn",
        "",
    ])
    return "\n".join(lines)
