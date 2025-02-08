import os
import warnings
import textwrap
import logging
from IPython.display import display, Markdown
from helper import load_env
from agents import create_agents, create_tasks, create_crew
from models import ContentOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    try:
        warnings.filterwarnings('ignore')
        load_env()
        
        required_env_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'
        return "groq/llama-3.1-70b-versatile"
    except Exception as e:
        logger.error(f"Environment setup failed: {str(e)}")
        raise

def validate_result(result):
    try:
        content_output = result.pydantic
        if not content_output.article or not content_output.social_media_posts:
            raise ValueError("Invalid content output: Missing article or social media posts")
        return True
    except Exception as e:
        logger.error(f"Content validation failed: {str(e)}")
        return False

def display_social_posts(result):
    posts = result.pydantic.dict()['social_media_posts']
    for post in posts:
        platform = post['platform']
        content = post['content']
        print(platform)
        wrapped_content = textwrap.fill(content, width=50)
        print(wrapped_content)
        print('-' * 50)

def display_blog_post(result):
    display(Markdown(result.pydantic.dict()['article']))

def main():
    try:
        # Setup
        groq_llm = setup_environment()
        logger.info("Environment setup completed")
        
        # Create agents and tasks
        agents = create_agents(groq_llm)
        tasks = create_tasks(agents)
        logger.info("Agents and tasks created")
        
        # Create and execute crew
        crew = create_crew(agents, tasks)
        result = crew.kickoff(inputs={
            'subject': 'Inflation in the US and the impact on the stock market in 2024'
        })
        
        # Validate and display results
        if validate_result(result):
            display_social_posts(result)
            display_blog_post(result)
            logger.info("Content generation completed successfully")
        else:
            logger.error("Content generation failed validation")
            
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
