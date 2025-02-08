#!/usr/bin/env python
# coding: utf-8

import datetime
import os
# from IPython.display import Image # REMOVE
import matplotlib.pyplot as plt  # ADD

from autogen import ConversableAgent, AssistantAgent

from MultiAgentFinancialAnalysis.stock_analysis import get_stock_prices, plot_stock_prices
from config import settings, configure_agents, configure_code_executor
from MultiAgentFinancialAnalysis.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Starting the financial analysis application")
    executor = configure_code_executor()
    code_executor_agent, code_writer_agent = configure_agents(executor)
    today = datetime.datetime.now().date()
    
    message1 = f"""Today is {today}.
Create a plot showing stock gain YTD for NVDA and TSLA.
Make sure the code is in markdown code block and save the figure to a file ytd_stock_gains.png."""
    
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message1,
    )
    
    # Image(os.path.join(settings.work_dir, "ytd_stock_gains.png")) # REMOVE
    image_path1 = os.path.join(settings.work_dir, "ytd_stock_gains.png")  # ADD
    print(f"Plot saved to: {image_path1}")  # ADD
    
    message2 = f"""Today is {today}.
Download the stock prices YTD for NVDA and TSLA and create a plot.
Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png."""
    
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message2,
    )
    
    # Image(os.path.join(settings.work_dir, "stock_prices_YTD_plot.png")) # REMOVE
    image_path2 = os.path.join(settings.work_dir, "stock_prices_YTD_plot.png")  # ADD
    print(f"Plot saved to: {image_path2}")  # ADD

if __name__ == '__main__':
    main()
