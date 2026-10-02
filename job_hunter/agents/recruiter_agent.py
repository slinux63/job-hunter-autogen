from __future__ import annotations

import autogen
from typing import Any


class RecruiterAgent:
    """Agent responsible for generating recruiter outreach messages."""

    def __init__(self, llm_config: dict[str, Any]):
        self.llm_config = llm_config
        self.agent = autogen.AssistantAgent(
            name="RecruiterOutreach",
            system_message="""You are an expert recruiter with years of experience. Your role is to:
1. Craft personalized application messages
2. Write compelling cover letters
3. Tailor professional pitches
4. Create LinkedIn outreach messages
5. Generate follow-up communication templates

When creating outreach content:
- Keep messages concise and impactful
- Personalize based on the company and role
- Highlight relevant experience
- Show genuine interest
- Include clear call-to-action
            """,
            llm_config=llm_config,
        )

    def generate_application_message(self, job: dict[str, Any], cv_summary: str) -> dict[str, str]:
        """Generate personalized application message for a job."""
        prompt = f"""Generate personalized application messages for this opportunity:

JOB DETAILS:
Title: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Description: {job.get('description', 'N/A')}

CANDIDATE SUMMARY:
{cv_summary}

Please generate:
1. A SHORT EMAIL (2-3 sentences) for direct application
2. A MEDIUM MESSAGE (1 paragraph) for recruiter outreach
3. A LINKEDIN MESSAGE (professional but friendly)
4. KEY POINTS TO HIGHLIGHT in conversation
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
            "outreach_content": self.agent.last_message()["content"],
        }

    def generate_cover_letter(self, job: dict[str, Any], cv_summary: str) -> str:
        """Generate a personalized cover letter."""
        prompt = f"""Write a compelling, personalized cover letter for this position:

JOB DETAILS:
Title: {job.get('title')}
Company: {job.get('company')}

CANDIDATE PROFILE:
{cv_summary}

Generate a professional cover letter that:
- Opens with genuine interest in the company
- Highlights relevant experience
- Shows understanding of role requirements
- Demonstrates cultural fit
- Ends with confident call-to-action

Format as a proper business letter (keep it 3-4 paragraphs).
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
