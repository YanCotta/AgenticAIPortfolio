#!/usr/bin/env python
# coding: utf-8

import datetime
import os
from IPython.display import Image

from autogen import ConversableAgent, AssistantAgent

from financial_analysis.stock_analysis import get_stock_prices, plot_stock_prices
from financial_analysis.config import settings
from financial_analysis.logger import get_logger

logger = get_logger(__name__)

llm_config = {"model": "gpt-4-turbo", "api_key": settings.openai_api_key}

def configure_executors():
    executor = LocalCommandLineCodeExecutor(
        timeout=settings.timeout,
        work_dir=settings.work_dir,
        functions=[get_stock_prices, plot_stock_prices],
    )
    return executor

def configure_agents(executor):
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

def main():
    logger.info("Starting the financial analysis application")
    executor = configure_executors()
    code_executor_agent, code_writer_agent = configure_agents(executor)
    today = datetime.datetime.now().date()
    
    message1 = f"""Today is {today}.
Create a plot showing stock gain YTD for NVDA and TSLA.
Make sure the code is in markdown code block and save the figure to a file ytd_stock_gains.png."""
    
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message1,
    )
    
    Image(os.path.join(settings.work_dir, "ytd_stock_gains.png"))
    
    message2 = f"""Today is {today}.
Download the stock prices YTD for NVDA and TSLA and create a plot.
Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png."""
    
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message2,
    )
    
    Image(os.path.join(settings.work_dir, "stock_prices_YTD_plot.png"))

if __name__ == '__main__':
    main()
