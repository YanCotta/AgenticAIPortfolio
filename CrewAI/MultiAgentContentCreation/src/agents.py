import yaml
import logging
from pathlib import Path
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from models import ContentOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_configs():
    try:
        config_dir = Path('config')
        files = {
            'agents': config_dir / 'agents.yaml',
            'tasks': config_dir / 'tasks.yaml'
        }
        
        configs = {}
        for config_type, file_path in files.items():
            if not file_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {file_path}")
                
            with open(file_path, 'r') as file:
                configs[config_type] = yaml.safe_load(file)
        
        return configs['agents'], configs['tasks']
    except Exception as e:
        logger.error(f"Error loading configurations: {str(e)}")
        raise

def create_agents(groq_llm):
    agents_config, _ = load_configs()
    
    market_news_monitor_agent = Agent(
        config=agents_config['market_news_monitor_agent'],
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        llm=groq_llm,
    )

    data_analyst_agent = Agent(
        config=agents_config['data_analyst_agent'],
        tools=[SerperDevTool(), WebsiteSearchTool()],
        llm=groq_llm,
    )

    content_creator_agent = Agent(
        config=agents_config['content_creator_agent'],
        tools=[SerperDevTool(), WebsiteSearchTool()],
    )

    quality_assurance_agent = Agent(
        config=agents_config['quality_assurance_agent'],
    )
    
    return (market_news_monitor_agent, data_analyst_agent, 
            content_creator_agent, quality_assurance_agent)

def create_tasks(agents):
    _, tasks_config = load_configs()
    market_news_monitor_agent, data_analyst_agent, content_creator_agent, quality_assurance_agent = agents
    
    monitor_financial_news_task = Task(
        config=tasks_config['monitor_financial_news'],
        agent=market_news_monitor_agent
    )

    analyze_market_data_task = Task(
        config=tasks_config['analyze_market_data'],
        agent=data_analyst_agent
    )

    create_content_task = Task(
        config=tasks_config['create_content'],
        agent=content_creator_agent,
        context=[monitor_financial_news_task, analyze_market_data_task]
    )

    quality_assurance_task = Task(
        config=tasks_config['quality_assurance'],
        agent=quality_assurance_agent,
        output_pydantic=ContentOutput
    )
    
    return (monitor_financial_news_task, analyze_market_data_task, 
            create_content_task, quality_assurance_task)

def create_crew(agents, tasks):
    try:
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )
        logger.info("Crew created successfully")
        return crew
    except Exception as e:
        logger.error(f"Error creating crew: {str(e)}")
        raise
