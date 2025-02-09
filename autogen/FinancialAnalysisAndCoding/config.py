"""
Module for configuring the agents and the code executor.
"""

import os
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from MultiAgentFinancialAnalysis.utils import get_openai_api_key
from MultiAgentFinancialAnalysis.logger import get_logger, configure_logger
from MultiAgentFinancialAnalysis.src.execution.code_executor import DockerCodeExecutor
from MultiAgentFinancialAnalysis.src.agents.analysis_agent import AnalysisAgent

logger = get_logger(__name__)

class Settings:
    """
    Settings class for the financial analysis application.
    """
    def __init__(self):
        self.openai_api_key = get_openai_api_key()
        self.work_dir = "coding"
        self.timeout = 60
        self.log_level = "INFO"
        configure_logger(self.log_level)  # Initialize logger here

settings = Settings()

def configure_llm():
    """Configures the language model with the OpenAI API key."""
    try:
        openai_api_key = settings.openai_api_key
        llm_config = {
            "model": "gpt-4-turbo",
            "api_key": openai_api_key,
        }
        return llm_config
    except ValueError as e:
        logger.error(f"Error configuring LLM: {e}")
        return None

def configure_code_executor(work_dir=settings.work_dir, timeout=settings.timeout, functions=None):
    """Configures the code executor with specified working directory, timeout, and functions."""
    if functions is None:
        functions = []
    executor = DockerCodeExecutor(
        timeout=timeout,
        work_dir=work_dir,
        functions=functions,
    )
    return executor

def configure_agents(executor):
    """Configures the AutoGen agents with the provided executor and language model configuration."""
    llm_config = configure_llm()
    if llm_config is None:
        logger.warning("LLM configuration is None. Agents may not function correctly.")

    code_executor_agent = ConversableAgent(
        name="code_executor_agent",
        llm_config=False,
        code_execution_config={"executor": executor},
        human_input_mode="ALWAYS",
        default_auto_reply="Please continue. If everything is done, reply 'TERMINATE'.",
    )

    code_writer_agent = AssistantAgent(
        name="code_writer_agent",
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    sys_msg = code_writer_agent.system_message
    sys_msg += executor.format_functions_for_prompt()

    code_writer_agent = ConversableAgent(
        name="code_writer_agent",
        system_message=sys_msg,
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    analysis_agent = AnalysisAgent(
        name="analysis_agent",
        llm_config=llm_config,
        plugins=["fundamentals", "news_sentiment", "social_media_signals"],
        human_input_mode="NEVER",
    )

    return code_executor_agent, code_writer_agent, analysis_agent
