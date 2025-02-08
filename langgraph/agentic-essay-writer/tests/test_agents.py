import pytest
from unittest.mock import AsyncMock
from ..src.agents.planner import PlannerAgent
from ..src.agents.researcher import ResearchAgent
from ..src.agents.writer import WriterAgent
from ..src.agents.critic import CriticAgent
from ..src.models.schema import AgentState
from ..src.config import Settings

@pytest.fixture
def mock_settings():
    settings = Settings()
    settings.MODEL_NAME = "test_model"
    return settings

@pytest.fixture
def mock_model():
    return AsyncMock()

@pytest.fixture
def mock_research_service():
    return AsyncMock()

@pytest.mark.asyncio
async def test_planner_agent(mock_settings, mock_model):
    mock_model.ainvoke.return_value.content = "Test Plan"
    planner = PlannerAgent(mock_settings, mock_model)
    state = AgentState(task="Test Task")
    result = await planner.execute(state)
    assert result["plan"] == "Test Plan"
    assert result["lnode"] == "planner"
    assert result["count"] == 1

@pytest.mark.asyncio
async def test_researcher_agent(mock_settings, mock_research_service, mock_model):
    mock_model.with_structured_output.return_value.ainvoke.return_value.queries = ["Test Query"]
    mock_research_service.search.return_value = {"results": [{"content": "Test Content"}]}
    researcher = ResearchAgent(mock_settings, mock_research_service, mock_model)
    state = AgentState(task="Test Task")
    result = await researcher.execute(state)
    assert "Test Content" in result["content"]
    assert result["lnode"] == "researcher"
    assert result["count"] == 1

@pytest.mark.asyncio
async def test_writer_agent(mock_settings, mock_model):
    mock_model.ainvoke.return_value.content = "Test Draft"
    writer = WriterAgent(mock_settings, mock_model)
    state = AgentState(task="Test Task", plan="Test Plan")
    result = await writer.execute(state)
    assert result["draft"] == "Test Draft"
    assert result["revision_number"] == 2
    assert result["lnode"] == "generate"
    assert result["count"] == 1

@pytest.mark.asyncio
async def test_critic_agent(mock_settings, mock_model):
    mock_model.ainvoke.return_value.content = "Test Critique"
    critic = CriticAgent(mock_settings, mock_model)
    state = AgentState(task="Test Task", draft="Test Draft")
    result = await critic.execute(state)
    assert result["critique"] == "Test Critique"
    assert result["lnode"] == "reflect"
    assert result["count"] == 1
