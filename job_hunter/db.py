from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable


class JobStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                salary TEXT,
                description TEXT,
                raw TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, url)
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                offer_id INTEGER,
                match_score INTEGER,
                fit_summary TEXT,
                missing_skills TEXT,
                action TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def save_offers(self, offers: Iterable[dict[str, Any]]) -> None:
        for offer in offers:
            self.conn.execute(
                """
                INSERT OR IGNORE INTO offers (source, title, company, location, url, salary, description, raw)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    offer.get("source"),
                    offer.get("title"),
                    offer.get("company"),
                    offer.get("location"),
                    offer.get("url"),
                    offer.get("salary"),
                    offer.get("description", ""),
                    json.dumps(offer, ensure_ascii=False),
                ),
            )
        self.conn.commit()

    def save_application(self, offer: dict[str, Any], match_score: int, fit_summary: str, missing_skills: str, action: str) -> None:
        offer_row = self.conn.execute(
            "SELECT id FROM offers WHERE source = ? AND url = ?",
            (offer.get("source"), offer.get("url")),
        ).fetchone()
        if not offer_row:
            return
        self.conn.execute(
            "INSERT INTO applications (offer_id, match_score, fit_summary, missing_skills, action) VALUES (?, ?, ?, ?, ?)",
            (offer_row["id"], match_score, fit_summary, missing_skills, action),
        )
        self.conn.commit()

    def save_summary(self, summary: str) -> None:
        self.conn.execute("INSERT INTO summaries (content) VALUES (?)", (summary,))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
