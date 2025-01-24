from crewai import Agent
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EditorAgent:
    @staticmethod
    def create(verbose: bool = True, tools: Optional[list] = None) -> Agent:
        """Create an editor agent with specified configuration."""
        try:
            return Agent(
                role="Editor",
                goal="Edit and refine content to ensure quality and accuracy",
                backstory="Expert editor specializing in technical content with a keen eye for detail.",
                allow_delegation=False,
                verbose=verbose,
                tools=tools or []
            )
        except Exception as e:
            logger.error(f"Error creating editor agent: {e}")
            raise

    @staticmethod
    def create_task(agent: Agent) -> Dict[str, Any]:
        """Create a task configuration for the editor agent."""
        return {
            "description": (
                "1. Review and refine the content for clarity and accuracy\n"
                "2. Ensure consistent tone and style\n"
                "3. Check for grammatical errors and improve readability\n"
                "4. Verify technical accuracy and citations\n"
                "5. Optimize content structure and flow"
            ),
            "expected_output": (
                "A polished, publication-ready document with proper "
                "formatting, clear structure, and accurate content."
            ),
            "agent": agent
        }
