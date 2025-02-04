import os
import warnings
import pandas as pd
from crewai import Crew
from .agents import create_agents_and_tasks
from .helper import load_env

warnings.filterwarnings('ignore')
load_env()

def setup_environment():
    os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

def format_project_inputs(project, objectives, industry, team_members, requirements):
    return {
        'project_type': project,
        'project_objectives': objectives,
        'industry': industry,
        'team_members': team_members,
        'project_requirements': requirements
    }

def run_project_planning(inputs):
    setup_environment()
    agents, tasks = create_agents_and_tasks()
    
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )
    
    result = crew.kickoff(inputs=inputs)
    
    # Calculate usage metrics
    costs = 0.150 * (crew.usage_metrics.prompt_tokens + crew.usage_metrics.completion_tokens) / 1_000_000
    print(f"Total costs: ${costs:.4f}")
    
    return result, crew.usage_metrics

if __name__ == "__main__":
    # Example usage
    project_inputs = format_project_inputs(
        project="Website",
        objectives="Create a website for a small business",
        industry="Technology",
        team_members="""
        - John Doe (Project Manager)
        - Jane Doe (Software Engineer)
        - Bob Smith (Designer)
        - Alice Johnson (QA Engineer)
        - Tom Brown (QA Engineer)
        """,
        requirements="""
        - Create a responsive design
        - Implement modern UI
        - Develop user-friendly navigation
        # ... more requirements ...
        """
    )
    
    result, metrics = run_project_planning(project_inputs)
    print(result.pydantic.dict())
