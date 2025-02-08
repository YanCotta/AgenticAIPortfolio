"""Tests for the multi-agent interactions."""

import pytest
from unittest.mock import MagicMock
# from autogen import ConversableAgent, AssistantAgent # REMOVE
# from autogen.coding import LocalCommandLineCodeExecutor # REMOVE
from MultiAgentFinancialAnalysis.config import configure_agents, configure_code_executor # ADD
from MultiAgentFinancialAnalysis.main import main # ADD

def test_configure_agents():
    """Test that agents are configured correctly."""
    executor = configure_code_executor()
    code_executor_agent, code_writer_agent = configure_agents(executor)

    assert code_executor_agent is not None
    assert code_writer_agent is not None
    assert code_executor_agent.name == "code_executor_agent"
    assert code_writer_agent.name == "code_writer_agent"

def test_main(monkeypatch, capsys):
    """Test the main function."""
    # Mock the initiate_chat method to avoid actual execution
    mock_agent = MagicMock()
    monkeypatch.setattr("MultiAgentFinancialAnalysis.main.configure_code_executor", lambda: None)
    monkeypatch.setattr("MultiAgentFinancialAnalysis.main.configure_agents", lambda executor: (mock_agent, mock_agent))
    monkeypatch.setattr("MultiAgentFinancialAnalysis.main.datetime.datetime", MagicMock(now=lambda: MagicMock(date=lambda: "2024-01-01")))
    mock_agent.initiate_chat.return_value = None

    # Run the main function
    main()

    # Capture the output
    captured = capsys.readouterr()

    # Assert that the plots are saved
    assert "Plot saved to: coding/ytd_stock_gains.png" in captured.out
    assert "Plot saved to: coding/stock_prices_YTD_plot.png" in captured.out
