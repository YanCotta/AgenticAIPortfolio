#!/usr/bin/env python
# coding: utf-8

# # Lesson 5: Coding and Financial Analysis

# ## Setup

import datetime
import os
from IPython.display import Image

# Import agent-related classes
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent, AssistantAgent

# Import analysis functions from the new module
from AgenticAIPortfolio.AutoGen.FinancialAnalysisAndCoding.src.analysis import get_stock_prices, plot_stock_prices

llm_config = {"model": "gpt-4-turbo"}

def configure_executors():
    # Configure the code executor with the user-defined functions from analysis module.
    executor = LocalCommandLineCodeExecutor(
        timeout=60,
        work_dir="coding",
        functions=[get_stock_prices, plot_stock_prices],
    )
    return executor

def configure_agents(executor):
    # Configure the agents using the executor.
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
    executor = configure_executors()
    code_executor_agent, code_writer_agent = configure_agents(executor)
    today = datetime.datetime.now().date()
    
    # First task: stock gains plot
    message1 = f"""Today is {today}.
Create a plot showing stock gain YTD for NVDA and TSLA.
Make sure the code is in markdown code block and save the figure to a file ytd_stock_gains.png."""
    
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message1,
    )
    
    # Display the generated plot for first task.
    Image(os.path.join("coding", "ytd_stock_gains.png"))
    
    # Second task: stock prices YTD plot using the new functions.
    message2 = f"""Today is {today}.
Download the stock prices YTD for NVDA and TSLA and create a plot.
Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png."""
    
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message2,
    )
    
    # Display the generated plot for second task.
    Image(os.path.join("coding", "stock_prices_YTD_plot.png"))

# ...existing code (if any)...

if __name__ == '__main__':
    main()
