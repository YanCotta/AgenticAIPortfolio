import yaml
from crewai import Agent, Task
from .models import ProjectPlan

def load_configs():
    files = {
        'agents': 'config/agents.yaml',
        'tasks': 'config/tasks.yaml'
    }
    
    configs = {}
    for config_type, file_path in files.items():
        with open(file_path, 'r') as file:
            configs[config_type] = yaml.safe_load(file)
    return configs['agents'], configs['tasks']

def create_agents_and_tasks():
    agents_config, tasks_config = load_configs()
    
    # Create Agents
    project_planning_agent = Agent(
        config=agents_config['project_planning_agent']
    )
    
    estimation_agent = Agent(
        config=agents_config['estimation_agent']
    )
    
    resource_allocation_agent = Agent(
        config=agents_config['resource_allocation_agent']
    )
    
    # Create Tasks
    tasks = [
        Task(
            config=tasks_config['task_breakdown'],
            agent=project_planning_agent
        ),
        Task(
            config=tasks_config['time_resource_estimation'],
            agent=estimation_agent
        ),
        Task(
            config=tasks_config['resource_allocation'],
            agent=resource_allocation_agent,
            output_pydantic=ProjectPlan
        )
    ]
    
    agents = [project_planning_agent, estimation_agent, resource_allocation_agent]
    
    return agents, tasks
