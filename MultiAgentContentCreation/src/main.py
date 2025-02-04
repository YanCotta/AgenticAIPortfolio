import os
import warnings
import textwrap
from IPython.display import display, Markdown
from helper import load_env
from agents import create_agents, create_tasks, create_crew

def setup_environment():
    warnings.filterwarnings('ignore')
    load_env()
    os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'
    return "groq/llama-3.1-70b-versatile"

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
    # Setup
    groq_llm = setup_environment()
    
    # Create agents and tasks
    agents = create_agents(groq_llm)
    tasks = create_tasks(agents)
    
    # Create and execute crew
    crew = create_crew(agents, tasks)
    result = crew.kickoff(inputs={
        'subject': 'Inflation in the US and the impact on the stock market in 2024'
    })
    
    # Display results
    display_social_posts(result)
    display_blog_post(result)

if __name__ == "__main__":
    main()
