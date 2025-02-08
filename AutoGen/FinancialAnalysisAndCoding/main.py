#!/usr/bin/env python
# coding: utf-8

import datetime
import os
from IPython.display import Image

# Import configuration functions
from config import configure_code_executor, configure_agents, configure_llm

# Import analysis functions
from stock_analysis import get_stock_prices, plot_stock_prices


def main():
    """
    Main function to orchestrate the stock analysis workflow using AutoGen agents.
    """
    llm_config = configure_llm()
    executor = configure_code_executor(functions=[get_stock_prices, plot_stock_prices])
    code_executor_agent, code_writer_agent = configure_agents(executor, llm_config)
    today = datetime.datetime.now().date()

    # Task 1: Stock gains plot
    message1 = f"""Today is {today}.
Create a plot showing stock gain YTD for NVDA and TSLA.
Make sure the code is in markdown code block and save the figure to a file ytd_stock_gains.png."""

    print("\nInitiating chat for task 1: Stock gains plot YTD...")
    chat_result1 = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message1,
    )

    # Display the generated plot for the first task.
    try:
        print("\nDisplaying plot for task 1...")
        Image(os.path.join("coding", "ytd_stock_gains.png"))
    except FileNotFoundError:
        print("Plot not found. Check the 'coding' directory.")

    # Task 2: Stock prices YTD plot using the new functions.
    message2 = f"""Today is {today}.
Download the stock prices YTD for NVDA and TSLA and create a plot.
Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png."""

    print("\nInitiating chat for task 2: Stock prices plot YTD using functions...")
    chat_result2 = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message2,
    )

    # Display the generated plot for the second task.
    try:
        print("\nDisplaying plot for task 2...")
        Image(os.path.join("coding", "stock_prices_YTD_plot.png"))
    except FileNotFoundError:
        print("Plot not found. Check the 'coding' directory.")


if __name__ == "__main__":
    main()
