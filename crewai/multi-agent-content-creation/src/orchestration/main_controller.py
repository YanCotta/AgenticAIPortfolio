import asyncio
import logging
from typing import List, Coroutine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainController:
    """
    Manages the asynchronous execution of tasks for a crew of agents.
    """
    def __init__(self, agents: list, tasks: list):
        self.agents = agents
        self.tasks = tasks
        self.agent_tasks = {agent: [] for agent in agents}

        # Assign tasks to agents based on task descriptions
        for task in tasks:
            self.assign_task(task)

    def assign_task(self, task):
        """
        Assigns a task to the appropriate agent based on the agent's capabilities
        described in the task's configuration.
        """
        agent = task.agent
        if agent in self.agents:
            self.agent_tasks[agent].append(task)
        else:
            logger.warning(f"No suitable agent found for task: {task.config['description']}")

    async def execute_task(self, task):
        """
        Asynchronously executes a given task.
        """
        try:
            logger.info(f"Executing task: {task.config['description']} with agent: {task.agent.role}")
            result = await task.execute()  # Assuming Task.execute is now an async method
            logger.info(f"Task completed: {task.config['description']}")
            return result
        except Exception as e:
            logger.error(f"Error executing task {task.config['description']}: {e}")
            return None

    async def run_crew(self, subject: str):
        """
        Orchestrates the execution of tasks by each agent asynchronously.
        """
        all_tasks = []
        for agent, tasks in self.agent_tasks.items():
            logger.info(f"Agent {agent.role} has tasks: {[task.config['description'] for task in tasks]}")
            for task in tasks:
                # Update the task's input with the subject
                task.config['description'] = task.config['description'].format(subject=subject)
                all_tasks.append(self.execute_task(task))

        results = await asyncio.gather(*all_tasks)
        return results
