#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, BaseTool
from utils import get_openai_api_key, pretty_print_result, get_serper_api_key
from typing import Tuple

def create_agents() -> Tuple[Agent, Agent]:
    sales_rep_agent = Agent(
        role="Sales Representative",
        goal="Identify high-value leads that match our ideal customer profile",
        backstory=(
            "As a part of the dynamic sales team at CrewAI, your mission is to scour "
            "the digital landscape for potential leads. Armed with cutting-edge tools "
            "and a strategic mindset, you analyze data, trends, and interactions to "
            "unearth opportunities that others might overlook. Your work is crucial in "
            "paving the way for meaningful engagements and driving the company's growth."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    lead_sales_rep_agent = Agent(
        role="Lead Sales Representative",
        goal="Nurture leads with personalized, compelling communications",
        backstory=(
            "Within the vibrant ecosystem of CrewAI's sales department, you stand out as "
            "the bridge between potential clients and the solutions they need. By creating "
            "engaging, personalized messages, you not only inform leads about our offerings "
            "but also make them feel seen and heard. Your role is pivotal in converting interest "
            "into action, guiding leads through the journey from curiosity to commitment."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    return sales_rep_agent, lead_sales_rep_agent

def create_tools() -> Tuple[BaseTool, BaseTool, BaseTool, BaseTool]:
    directory_read_tool = DirectoryReadTool(directory='./instructions')
    file_read_tool = FileReadTool()
    search_tool = SerperDevTool()
    
    class SentimentAnalysisTool(BaseTool):
        name: str = "Sentiment Analysis Tool"
        description: str = "Analyzes the sentiment of text to ensure positive and engaging communication."
        
        def _run(self, text: str) -> str:
            # Your custom code tool goes here
            return "positive"
    
    sentiment_analysis_tool = SentimentAnalysisTool()
    return directory_read_tool, file_read_tool, search_tool, sentiment_analysis_tool

def create_tasks(
    tools: Tuple[BaseTool, BaseTool, BaseTool, BaseTool],
    agents: Tuple[Agent, Agent]
) -> Tuple[Task, Task]:
    directory_read_tool, file_read_tool, search_tool, sentiment_analysis_tool = tools
    sales_rep_agent, lead_sales_rep_agent = agents
    
    lead_profiling_task = Task(
        description=(
            "Conduct an in-depth analysis of {lead_name}, a company in the {industry} sector "
            "that recently showed interest in our solutions. Utilize all available data sources "
            "to compile a detailed profile, focusing on key decision-makers, recent business "
            "developments, and potential needs that align with our offerings. This task is crucial "
            "for tailoring our engagement strategy effectively.\nDon't make assumptions and "
            "only use information you absolutely sure about."
        ),
        expected_output=(
            "A comprehensive report on {lead_name}, including company background, key personnel, "
            "recent milestones, and identified needs. Highlight potential areas where our solutions "
            "can provide value, and suggest personalized engagement strategies."
        ),
        tools=[directory_read_tool, file_read_tool, search_tool],
        agent=sales_rep_agent,
    )
    
    personalized_outreach_task = Task(
        description=(
            "Using the insights gathered from the lead profiling report on {lead_name}, craft a personalized "
            "outreach campaign aimed at {key_decision_maker}, the {position} of {lead_name}. The campaign should "
            "address their recent {milestone} and how our solutions can support their goals. Your communication must "
            "resonate with {lead_name}'s company culture and values, demonstrating a deep understanding of their business "
            "and needs.\nDon't make assumptions and only use information you absolutely sure about."
        ),
        expected_output=(
            "A series of personalized email drafts tailored to {lead_name}, specifically targeting {key_decision_maker}. "
            "Each draft should include a compelling narrative that connects our solutions with their recent achievements "
            "and future goals. Ensure the tone is engaging, professional, and aligned with {lead_name}'s corporate identity."
        ),
        tools=[sentiment_analysis_tool, search_tool],
        agent=lead_sales_rep_agent,
    )
    
    return lead_profiling_task, personalized_outreach_task

def create_crew(agents: Tuple[Agent, Agent], tasks: Tuple[Task, Task]) -> Crew:
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2,
        memory=True
    )
    return crew

def main() -> None:
    agents = create_agents()
    tools = create_tools()
    tasks = create_tasks(tools, agents)
    crew = create_crew(agents, tasks)
    
    inputs = {
        "lead_name": "DeepLearningAI",
        "industry": "Online Learning Platform",
        "key_decision_maker": "Andrew Ng",
        "position": "CEO",
        "milestone": "product launch"
    }
    
    result = crew.kickoff(inputs=inputs)
    
    from IPython.display import Markdown
    Markdown(pretty_print_result(result))

if __name__ == "__main__":
    main()
