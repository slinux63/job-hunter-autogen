from __future__ import annotations

import autogen
from typing import Any
from pathlib import Path

from job_hunter.config import get_settings
from job_hunter.agents import (
    JobCollectorAgent,
    CVAnalyzerAgent,
    MatcherAgent,
    DigestAgent,
    RecruiterAgent,
)


class JobHuntOrchestrator:
    """Main orchestrator that coordinates multiple agents for job hunting."""

    def __init__(self, llm_config: dict[str, Any] | None = None):
        self.settings = get_settings()
        
        if llm_config is None:
            llm_config = {
                "model": self.settings.lmstudio_model,
                "api_key": "unused",
                "base_url": self.settings.lmstudio_base_url,
                "api_type": "open_ai",
                "temperature": 0.7,
            }
        
        self.llm_config = llm_config
        
        # Initialize all agents
        self.collector = JobCollectorAgent(llm_config)
        self.cv_analyzer = CVAnalyzerAgent(llm_config)
        self.matcher = MatcherAgent(llm_config)
        self.digest_gen = DigestAgent(llm_config)
        self.recruiter = RecruiterAgent(llm_config)
        
        # Setup multi-agent group chat
        self._setup_group_chat()

    def _setup_group_chat(self) -> None:
        """Setup a group chat between all agents."""
        self.agents = [
            self.collector.agent,
            self.cv_analyzer.agent,
            self.matcher.agent,
            self.digest_gen.agent,
            self.recruiter.agent,
        ]
        
        self.groupchat = autogen.GroupChat(
            agents=self.agents,
            messages=[],
            max_turns=10,
            speaker_selection_method="round_robin",
        )
        
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config,
        )

    def run_full_workflow(self, keywords: str | None = None, location: str | None = None, limit: int | None = None) -> dict[str, Any]:
        """Run the full job hunting workflow with all agents."""
        
        if keywords is None:
            keywords = self.settings.job_keywords
        if location is None:
            location = self.settings.job_location
        if limit is None:
            limit = self.settings.max_results
        
        print("\n" + "="*70)
        print("🚀 STARTING MULTI-AGENT JOB HUNT WORKFLOW")
        print("="*70 + "\n")
        
        # Step 1: Collect jobs
        print("[Step 1] Job Collection")
        print("-" * 70)
        jobs = self.collector.collect_jobs(keywords, location, limit, self.settings.db_path)
        print(f"✅ Collected {len(jobs)} job opportunities\n")
        
        # Step 2: Analyze CV
        print("[Step 2] CV Analysis")
        print("-" * 70)
        cv_analysis = self.cv_analyzer.analyze_cv(self.settings.cv_path)
        cv_summary = self.cv_analyzer.extract_skills(self.settings.cv_path)
        print(f"✅ CV analyzed. Found {len(cv_summary)} key skills\n")
        
        # Step 3: Match jobs
        print("[Step 3] Job Matching")
        print("-" * 70)
        matches = self.matcher.batch_match_jobs(jobs, cv_analysis)
        print(f"✅ Matched {len(matches)} jobs against profile\n")
        
        # Step 4: Generate digest
        print("[Step 4] Digest Generation")
        print("-" * 70)
        cv_summary_text = f"Key Skills: {', '.join(cv_summary)}\n{cv_analysis.get('analysis', 'N/A')}"
        digest = self.digest_gen.generate_digest(matches, cv_summary_text)
        self.digest_gen.save_digest(digest, self.settings.db_path.replace('.db', '_digest.md'))
        print(f"✅ Daily digest generated\n")
        
        # Step 5: Generate recruiter outreach (for top 3)
        print("[Step 5] Recruiter Outreach Generation")
        print("-" * 70)
        top_jobs = jobs[:3]
        outreach_messages = []
        for job in top_jobs:
            try:
                msg = self.recruiter.generate_application_message(job, cv_summary_text)
                outreach_messages.append(msg)
            except Exception as e:
                print(f"Could not generate outreach for {job.get('title')}: {e}")
        print(f"✅ Generated {len(outreach_messages)} outreach messages\n")
        
        print("="*70)
        print("✅ WORKFLOW COMPLETE")
        print("="*70 + "\n")
        
        return {
            "jobs_collected": len(jobs),
            "matches": len(matches),
            "digest": digest,
            "outreach_messages": outreach_messages,
            "cv_skills": cv_summary,
        }

    def run_group_chat_workflow(self, query: str) -> None:
        """Run an interactive group chat with all agents."""
        print("\n" + "="*70)
        print("🗣️ STARTING MULTI-AGENT GROUP CHAT")
        print("="*70 + "\n")
        
        user_proxy = autogen.UserProxyAgent(
            name="HRManager",
            human_input_mode="NEVER",
            system_message="You are an HR manager coordinating a job search. Provide clear directives to the team.",
        )
        
        user_proxy.initiate_chat(
            self.manager,
            message=query,
            max_turns=5,
        )
