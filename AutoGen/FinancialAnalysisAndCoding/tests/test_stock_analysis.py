"""Tests for the stock_analysis module."""

import pandas as pd
from MultiAgentFinancialAnalysis.stock_analysis import get_stock_prices, plot_stock_prices
from unittest.mock import patch

def test_get_stock_prices_success(mock_yfinance_download):
    """Tests successful retrieval of stock prices."""
    mock_yfinance_download.return_value = pd.DataFrame({"Close": [1, 2, 3]})
    stock_prices = get_stock_prices("NVDA", "2024-01-01", "2024-01-03")
    assert not stock_prices.empty
    assert len(stock_prices) == 3

def test_get_stock_prices_empty(mock_yfinance_download):
    """Tests handling of empty stock prices."""
    mock_yfinance_download.return_value = pd.DataFrame()
    stock_prices = get_stock_prices("INVALID", "2024-01-01", "2024-01-03")
    assert stock_prices.empty

@patch("financial_analysis.stock_analysis.plt")
def test_plot_stock_prices_success(mock_plt):
    """Tests successful plotting of stock prices."""
    stock_prices = pd.DataFrame({"NVDA": [1, 2, 3]})
    plot_stock_prices(stock_prices, filename="test.png")
    mock_plt.savefig.assert_called_once_with("test.png")

@patch("financial_analysis.stock_analysis.plt")
def test_plot_stock_prices_empty(mock_plt):
    """Tests handling of empty stock prices for plotting."""
    stock_prices = pd.DataFrame()
    plot_stock_prices(stock_prices, filename="test.png")
    mock_plt.savefig.assert_not_called()
