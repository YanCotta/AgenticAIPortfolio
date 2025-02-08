import pytest
from unittest.mock import patch, MagicMock
from src.main import ContentCreationSystem
import os

@pytest.fixture
def content_system():
    with patch('src.main.get_api_key') as mock_get_key:
        mock_get_key.return_value = "fake-api-key"
        system = ContentCreationSystem()
        yield system

def test_content_system_initialization(content_system):
    assert content_system.agents
    assert content_system.tasks
    assert content_system.crew

@patch('src.main.get_api_key')
def test_environment_setup_error(mock_get_key):
    mock_get_key.return_value = None
    with pytest.raises(EnvironmentError):
        ContentCreationSystem()

def test_agent_creation(content_system):
    assert "planner" in content_system.agents
    assert "writer" in content_system.agents
    assert "editor" in content_system.agents

@pytest.mark.integration
def test_content_generation_flow(content_system):
    with patch.object(content_system.crew, 'kickoff') as mock_kickoff:
        mock_kickoff.return_value = "Test content"
        result = content_system.generate_content("AI")
        assert isinstance(result, str)
        mock_kickoff.assert_called_once_with(inputs={"topic": "AI"})

def test_error_handling_in_content_generation(content_system):
    with patch.object(content_system.crew, 'kickoff', 
                     side_effect=Exception("Test error")):
        with pytest.raises(Exception):
            content_system.generate_content("AI")
