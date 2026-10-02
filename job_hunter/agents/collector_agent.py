from __future__ import annotations

import autogen
from typing import Any

from job_hunter.sources import fetch_public_jobs
from job_hunter.db import JobStore


class JobCollectorAgent:
    """Agent responsible for collecting job offers from public sources."""

    def __init__(self, llm_config: dict[str, Any]):
        self.llm_config = llm_config
        self.agent = autogen.AssistantAgent(
            name="JobCollector",
            system_message="""You are a job collection specialist. Your role is to:
1. Identify the best search terms for a given job role
2. Suggest optimal search locations
3. Recommend job sources to search
4. Summarize collected job data in a structured format

When given a job search request, analyze it and provide recommendations for effective job hunting.
            """,
            llm_config=llm_config,
        )

    def collect_jobs(self, keywords: str, location: str, limit: int = 10, db_path: str = "data/job_hunter.db") -> list[dict[str, Any]]:
        """Collect jobs from public sources and save to database."""
        print(f"[JobCollector] Collecting jobs for: {keywords} in {location}")
        
        jobs = fetch_public_jobs(keywords, location, limit=limit)
        store = JobStore(db_path)
        store.save_offers(jobs)
        store.close()
        
        return jobs

    def analyze_search_strategy(self, role: str, level: str = "mid") -> str:
        """Ask the agent to analyze and suggest search strategy."""
        prompt = f"""Analyze the best job search strategy for the following:
- Role: {role}
- Experience Level: {level}

Provide recommendations on:
1. Best search keywords
2. Relevant job sources
3. Geographic focus areas
4. Key skills to highlight
        """
        
        user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
        )
        
        user_proxy.initiate_chat(
            self.agent,
            message=prompt,
            max_turns=2,
        )
        
        return self.agent.last_message()["content"]
