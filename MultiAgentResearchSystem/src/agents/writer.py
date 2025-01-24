from crewai import Agent
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class WriterAgent:
    @staticmethod
    def create(verbose: bool = True, tools: Optional[list] = None) -> Agent:
        """Create a writer agent with specified configuration."""
        try:
            return Agent(
                role="Content Writer",
                goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
                backstory="You're working on writing a new opinion piece about the topic: {topic}. "
                         "You base your writing on the work of the Content Planner.",
                allow_delegation=False,
                verbose=verbose,
                tools=tools or []
            )
        except Exception as e:
            logger.error(f"Error creating writer agent: {e}")
            raise

    @staticmethod
    def create_task(agent: Agent) -> Dict[str, Any]:
        """Create a task configuration for the writer agent."""
        return {
            "description": (
                "1. Use the content plan to craft a compelling "
                    "blog post on {topic}.\n"
                "2. Incorporate SEO keywords naturally.\n"
                "3. Sections/Subtitles are properly named "
                    "in an engaging manner.\n"
                "4. Ensure the post is structured with an "
                    "engaging introduction, insightful body, "
                    "and a summarizing conclusion."
            ),
            "expected_output": (
                "A well-written blog post in markdown format, "
                "ready for publication, each section should "
                "have 2 or 3 paragraphs."
            ),
            "agent": agent
        }
