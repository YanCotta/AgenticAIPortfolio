from typing import Dict, List
import os
from crewai import Task, Crew, Agent
from agents.planner import PlannerAgent
from agents.writer import WriterAgent
from agents.editor import EditorAgent
from utils.helpers import get_api_key, pretty_print_result
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentCreationSystem:
    def __init__(self) -> None:
        self.setup_environment()
        self.agents: Dict[str, Agent] = self.create_agents()
        self.tasks: List[Task] = self.create_tasks()
        self.crew: Crew = self.create_crew()

    def setup_environment(self) -> None:
        """Initialize environment variables."""
        api_key = get_api_key("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not found")
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
        logger.info("Environment setup completed")

    def create_agents(self) -> Dict[str, Agent]:
        """Create and return agent instances."""
        try:
            return {
                "planner": PlannerAgent.create(),
                "writer": WriterAgent.create(),
                "editor": EditorAgent.create()
            }
        except Exception as e:
            logger.error(f"Error creating agents: {e}")
            raise

    def create_tasks(self) -> List[Task]:
        tasks = []
        for agent_name, agent in self.agents.items():
            task_data = getattr(
                globals()[f"{agent_name.capitalize()}Agent"],
                "create_task"
            )(agent)
            tasks.append(Task(**task_data))
        return tasks

    def create_crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=2
        )

    def generate_content(self, topic: str) -> str:
        try:
            result = self.crew.kickoff(inputs={"topic": topic})
            return pretty_print_result(result)
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise

if __name__ == "__main__":
    system = ContentCreationSystem()
    topic = input("Enter a topic for content creation: ")
    result = system.generate_content(topic)
    print(result)
