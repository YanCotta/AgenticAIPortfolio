"""Pytest fixtures for the financial analysis project."""

import pytest
from unittest.mock import MagicMock
from financial_analysis.config import Settings

@pytest.fixture
def mock_settings() -> Settings:
    """Mocks the settings for testing."""
    settings = Settings(openai_api_key="test_key", log_level="DEBUG", timeout=10)
    return settings

@pytest.fixture
def mock_yfinance_download() -> MagicMock:
    """Mocks the yfinance.download function."""
    with MagicMock() as mock:
        yield mock
