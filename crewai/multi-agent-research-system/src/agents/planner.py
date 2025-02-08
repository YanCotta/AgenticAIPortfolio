from crewai import Agent
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class PlannerAgent:
    @staticmethod
    def create(verbose: bool = True, tools: Optional[list] = None) -> Agent:
        """Create a planner agent with specified configuration."""
        try:
            return Agent(
                role="Content Planner",
                goal="Plan engaging and factually accurate content on {topic}",
                backstory="You're working on planning a blog article "
                         "about the topic: {topic}. "
                         "You collect information that helps the "
                         "audience learn something "
                         "and make informed decisions.",
                allow_delegation=False,
                verbose=verbose,
                tools=tools or []
            )
        except Exception as e:
            logger.error(f"Error creating planner agent: {e}")
            raise

    @staticmethod
    def create_task(agent: Agent) -> Dict[str, Any]:
        """Create a task configuration for the planner agent."""
        return {
            "description": (
                "1. Prioritize the latest trends, key players, "
                    "and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering "
                    "their interests and pain points.\n"
                "3. Develop a detailed content outline including "
                    "an introduction, key points, and a call to action.\n"
                "4. Include SEO keywords and relevant data or sources."
            ),
            "expected_output": (
                "A comprehensive content plan document "
                "with an outline, audience analysis, "
                "SEO keywords, and resources."
            ),
            "agent": agent
        }
