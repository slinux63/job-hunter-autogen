from __future__ import annotations

import autogen
from typing import Any
from pathlib import Path


class CVAnalyzerAgent:
    """Agent responsible for analyzing CV and extracting key information."""

    def __init__(self, llm_config: dict[str, Any]):
        self.llm_config = llm_config
        self.agent = autogen.AssistantAgent(
            name="CVAnalyzer",
            system_message="""You are an expert CV and talent analyst. Your role is to:
1. Extract and analyze key skills from a CV
2. Identify gaps in technical knowledge
3. Assess experience level and seniority
4. Recommend skill improvements
5. Suggest roles that match the profile

When analyzing a CV, provide structured insights about strengths, gaps, and opportunities.
            """,
            llm_config=llm_config,
        )

    def load_cv(self, cv_path: str) -> str:
        """Load CV from file."""
        file_path = Path(cv_path)
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return "No CV found"

    def analyze_cv(self, cv_path: str) -> dict[str, Any]:
        """Analyze CV and extract key information."""
        print(f"[CVAnalyzer] Analyzing CV from: {cv_path}")
        
        cv_content = self.load_cv(cv_path)
        prompt = f"""Please analyze the following CV and provide structured insights:

{cv_content}

Provide your analysis in the following format:
- SKILLS: List of technical skills
- EXPERIENCE_LEVEL: Junior/Mid/Senior
- STRENGTHS: Top 3 strengths
- GAPS: Top 3 skill gaps
- RECOMMENDATIONS: How to improve marketability
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
        
        analysis = self.agent.last_message()["content"]
        return {
            "cv_path": cv_path,
            "analysis": analysis,
        }

    def extract_skills(self, cv_path: str) -> list[str]:
        """Extract skills from CV using keyword matching."""
        cv_content = self.load_cv(cv_path)
        cv_lower = cv_content.lower()
        
        common_skills = [
            "python", "javascript", "java", "c++", "rust",
            "sql", "mongodb", "postgresql", "redis",
            "fastapi", "django", "flask", "nodejs", "react", "vue",
            "docker", "kubernetes", "aws", "azure", "gcp",
            "git", "jenkins", "gitlab-ci", "github-actions",
            "rest", "graphql", "websocket",
            "microservices", "architecture", "design patterns",
        ]
        
        found_skills = [skill for skill in common_skills if skill in cv_lower]
        return found_skills
