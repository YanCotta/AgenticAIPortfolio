"""Tests for the stock_analysis module."""

import pytest
import pandas as pd
from unittest.mock import patch
from MultiAgentFinancialAnalysis.stock_analysis import get_stock_prices, plot_stock_prices

def test_get_stock_prices():
    """Test the get_stock_prices function."""
    # Test with valid stock symbols
    stock_prices = get_stock_prices(stock_symbols=["NVDA", "TSLA"], start_date="2023-01-01", end_date="2023-01-10")
    assert isinstance(stock_prices, pd.DataFrame)
    assert not stock_prices.empty

    # Test with invalid stock symbols
    stock_prices = get_stock_prices(stock_symbols=["INVALID"], start_date="2023-01-01", end_date="2023-01-10")
    assert isinstance(stock_prices, pd.DataFrame)
    assert stock_prices.empty

@patch("MultiAgentFinancialAnalysis.stock_analysis.plt")
def test_plot_stock_prices(mock_plt):
    """Test the plot_stock_prices function."""
    # Create a sample DataFrame
    data = {'NVDA': [100, 101, 102], 'TSLA': [200, 201, 202]}
    stock_prices = pd.DataFrame(data)
    stock_prices.index = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])

    # Call the function
    plot_stock_prices(stock_prices, filename="test_plot.png")

    # Assert that the plot was saved
    mock_plt.savefig.assert_called_once_with("test_plot.png")
