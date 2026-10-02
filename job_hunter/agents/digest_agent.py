from __future__ import annotations

import autogen
from typing import Any
from datetime import datetime


class DigestAgent:
    """Agent responsible for generating daily digest and recommendations."""

    def __init__(self, llm_config: dict[str, Any]):
        self.llm_config = llm_config
        self.agent = autogen.AssistantAgent(
            name="DigestGenerator",
            system_message="""You are an expert job search coach and strategist. Your role is to:
1. Synthesize job matching results into actionable insights
2. Prioritize opportunities based on career goals
3. Generate personalized daily digests
4. Provide application strategy recommendations
5. Create follow-up action plans

When generating a digest, provide:
- Top opportunities to pursue
- Medium-priority opportunities
- Opportunities to skip
- Daily action items
- Long-term strategy recommendations
            """,
            llm_config=llm_config,
        )

    def generate_digest(self, matches: list[dict[str, Any]], cv_summary: str) -> str:
        """Generate a daily job search digest."""
        print("[DigestGenerator] Generating daily digest...")
        
        matches_text = "\n".join([
            f"- {m.get('job_title')} @ {m.get('company')}: {m.get('matching_analysis', 'N/A')[:200]}..."
            for m in matches[:10]
        ])
        
        prompt = f"""Based on the following job matching results and candidate profile, generate a strategic daily digest:

CANDIDATE PROFILE SUMMARY:
{cv_summary}

TODAY'S MATCHED OPPORTUNITIES:
{matches_text}

Please generate a comprehensive daily digest that includes:

1. EXECUTIVE SUMMARY
   - Number of matches analyzed
   - Best opportunity rating

2. TOP 3 PRIORITIES
   - Jobs to apply for today
   - Why each is a good fit
   - Action steps

3. SECONDARY OPPORTUNITIES
   - Roles worth considering
   - Skill improvements needed

4. TODAY'S ACTION PLAN
   - Immediate tasks
   - CV tailoring needed
   - Follow-ups required

5. LONG-TERM STRATEGY
   - Skills to develop
   - Target companies to watch
   - Next steps for career growth
        """
        
        user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
        )
        
        user_proxy.initiate_chat(
            self.agent,
            message=prompt,
            max_turns=3,
        )
        
        digest = self.agent.last_message()["content"]
        return digest

    def save_digest(self, digest: str, output_path: str = "data/daily_digest.md") -> None:
        """Save digest to file with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"# Daily Job Hunt Digest\n\n*Generated: {timestamp}*\n\n{digest}"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"[DigestGenerator] Digest saved to {output_path}")
