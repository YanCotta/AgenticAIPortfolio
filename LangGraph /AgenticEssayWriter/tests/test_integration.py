import pytest
from unittest.mock import AsyncMock
from ..src.workflow.essay_workflow import EssayWorkflow
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
async def test_essay_workflow(mock_settings, mock_model, mock_research_service):
    mock_model.ainvoke.return_value.content = "Test Plan"
    mock_model.with_structured_output.return_value.ainvoke.return_value.queries = ["Test Query"]
    mock_research_service.search.return_value = {"results": [{"content": "Test Content"}]}
    mock_model.ainvoke.return_value.content = "Test Draft"
    mock_model.ainvoke.return_value.content = "Test Critique"

    planner = PlannerAgent(mock_settings, mock_model)
    researcher = ResearchAgent(mock_settings, mock_research_service, mock_model)
    writer = WriterAgent(mock_settings, mock_model)
    critic = CriticAgent(mock_settings, mock_model)
    workflow = EssayWorkflow(planner, researcher, writer, critic)

    state = await workflow.generate_essay("Test Task")

    assert state.plan == "Test Plan"
    assert "Test Content" in state.content
    assert state.draft == "Test Draft"
    assert state.critique == "Test Critique"
