"""
Module for downloading stock data and generating stock plots.
"""

import yfinance
import matplotlib.pyplot as plt
import pandas as pd

def get_stock_prices(stock_symbols, start_date, end_date):
    """
    Retrieves historical stock prices for the given symbols within the specified date range.

    Args:
        stock_symbols (str or list): A string or list of stock symbols (e.g., "NVDA" or ["NVDA", "TSLA"]).
        start_date (str): The start date for the data in "YYYY-MM-DD" format.
        end_date (str): The end date for the data in "YYYY-MM-DD" format.

    Returns:
        pandas.DataFrame: A DataFrame containing the closing prices for each stock symbol, indexed by date.
                          Returns an empty DataFrame if no data is found or an error occurs.
    """
    try:
        stock_data = yfinance.download(stock_symbols, start=start_date, end=end_date)
        if stock_data.empty:
            print(f"Warning: No data found for symbols: {stock_symbols}")
            return pd.DataFrame()
        return stock_data["Close"]
    except Exception as e:
        print(f"Error fetching stock data for {stock_symbols}: {e}")
        return pd.DataFrame()

def plot_stock_prices(stock_prices, filename="stock_prices.png"):
    """
    Plots the historical stock prices for the given symbols and saves the plot to a file.

    Args:
        stock_prices (pandas.DataFrame): A DataFrame containing the stock prices, with columns representing
                                         different stock symbols and the index representing the date.
        filename (str, optional): The name of the file to save the plot to (e.g., "stock_prices.png").
                                   Defaults to "stock_prices.png".
    """
    if stock_prices.empty:
        print("Warning: No stock prices to plot.  Ensure data was successfully retrieved.")
        return

    plt.figure(figsize=(12, 6))  # Adjust figure size for better readability
    for column in stock_prices.columns:
        plt.plot(stock_prices.index, stock_prices[column], label=column)

    plt.title("Historical Stock Prices", fontsize=16)  # More prominent title
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price (USD)", fontsize=12)  # Added units
    plt.grid(True, linestyle='--', alpha=0.5)  # More subtle grid
    plt.legend(loc='upper left', fontsize=10)  # Adjusted legend location and size
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping

    try:
        plt.savefig(filename)
        print(f"Plot saved to {filename}")
    except Exception as e:
        print(f"Error saving plot: {e}")
    finally:
        plt.close()  # Close the plot to prevent memory leaks
