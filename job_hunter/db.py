from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    lmstudio_base_url: str = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    lmstudio_model: str = os.getenv("LMSTUDIO_MODEL", "mistral")
    job_keywords: str = os.getenv("JOB_KEYWORDS", "python backend")
    job_location: str = os.getenv("JOB_LOCATION", "Paris")
    db_path: str = os.getenv("DB_PATH", "data/job_hunter.db")
    cv_path: str = os.getenv("CV_PATH", "data/cv.md")
    max_results: int = int(os.getenv("MAX_RESULTS", "10"))


def get_settings() -> Settings:
    return Settings()


def ensure_dirs() -> None:
    Path(os.getenv("DB_PATH", "data/job_hunter.db")).parent.mkdir(parents=True, exist_ok=True)
    Path(os.getenv("CV_PATH", "data/cv.md")).parent.mkdir(parents=True, exist_ok=True)
