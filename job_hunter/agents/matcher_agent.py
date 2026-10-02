from __future__ import annotations

import autogen
from typing import Any


class MatcherAgent:
    """Agent responsible for matching jobs with CV."""

    def __init__(self, llm_config: dict[str, Any]):
        self.llm_config = llm_config
        self.agent = autogen.AssistantAgent(
            name="JobMatcher",
            system_message="""You are an expert job matching specialist. Your role is to:
1. Compare job requirements with candidate profiles
2. Score job fit based on multiple factors
3. Identify skill gaps for specific roles
4. Provide personalized recommendations
5. Rank opportunities by relevance

When matching jobs to CVs, consider:
- Technical skill alignment
- Experience level match
- Career growth potential
- Compensation expectations
- Work culture fit (if available)
            """,
            llm_config=llm_config,
        )

    def match_job_to_cv(self, job: dict[str, Any], cv_analysis: dict[str, Any]) -> dict[str, Any]:
        """Match a specific job to a CV profile."""
        prompt = f"""Match the following job to the candidate profile:

JOB OFFER:
Title: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Description: {job.get('description', 'N/A')}
Salary: {job.get('salary', 'Not specified')}

CANDIDATE ANALYSIS:
{cv_analysis.get('analysis', 'N/A')}

Provide:
1. Match Score (0-100%)
2. Fit Assessment (Strong/Good/Moderate/Weak)
3. Top 3 Matching Skills
4. Top 3 Missing Skills
5. Recommendation (Apply/Consider/Skip)
6. Brief explanation of the match
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
        
        return {
            "job_title": job.get('title'),
            "company": job.get('company'),
            "matching_analysis": self.agent.last_message()["content"],
        }

    def batch_match_jobs(self, jobs: list[dict[str, Any]], cv_analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Match multiple jobs to CV."""
        results = []
        for job in jobs:
            try:
                match = self.match_job_to_cv(job, cv_analysis)
                results.append(match)
            except Exception as e:
                print(f"Error matching {job.get('title')}: {e}")
                continue
        return results
