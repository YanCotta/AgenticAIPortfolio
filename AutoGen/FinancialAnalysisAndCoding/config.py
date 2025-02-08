"""
Module for configuring the agents and the code executor.
"""

import os
from dotenv import load_dotenv, find_dotenv
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor

def load_env():
    """Loads environment variables from a .env file."""
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    """
    Retrieves the OpenAI API key from the environment variables.

    Raises:
        ValueError: If the OPENAI_API_KEY is not found in the environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.  Please set it in a .env file.")
    return openai_api_key

def configure_llm():
    """Configures the language model with the OpenAI API key."""
    try:
        openai_api_key = get_openai_api_key()
        llm_config = {
            "model": "gpt-4-turbo",
            "api_key": openai_api_key,
        }
        return llm_config
    except ValueError as e:
        print(f"Error configuring LLM: {e}")
        return None  # Or raise the exception, depending on desired behavior

def configure_code_executor(work_dir="coding", timeout=60, functions=None):
    """Configures the code executor with specified working directory, timeout, and functions."""
    if functions is None:
        functions = []
    executor = LocalCommandLineCodeExecutor(
        timeout=timeout,
        work_dir=work_dir,
        functions=functions,
    )
    return executor

def configure_agents(executor, llm_config):
    """Configures the AutoGen agents with the provided executor and language model configuration."""
    if llm_config is None:
        print("Warning: LLM configuration is None. Agents may not function correctly.")
        # Consider raising an exception or returning default agents

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

    return code_executor_agent, code_writer_agent
