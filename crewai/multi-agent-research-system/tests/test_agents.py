import pytest
from unittest.mock import patch, MagicMock
from src.agents.planner import PlannerAgent
from src.agents.writer import WriterAgent
from src.agents.editor import EditorAgent
from crewai import Agent

def test_planner_agent_creation():
    agent = PlannerAgent.create(verbose=False)
    assert isinstance(agent, Agent)
    assert agent.role == "Content Planner"

def test_writer_agent_creation():
    agent = WriterAgent.create(verbose=False)
    assert isinstance(agent, Agent)
    assert agent.role == "Content Writer"

def test_editor_agent_creation():
    agent = EditorAgent.create(verbose=False)
    assert isinstance(agent, Agent)
    assert agent.role == "Editor"

def test_planner_task_creation():
    agent = PlannerAgent.create(verbose=False)
    task_data = PlannerAgent.create_task(agent)
    assert isinstance(task_data, dict)
    assert "description" in task_data
    assert "expected_output" in task_data
    assert "agent" in task_data

@pytest.mark.parametrize("AgentClass", [
    PlannerAgent,
    WriterAgent,
    EditorAgent
])
def test_agent_task_creation(AgentClass):
    agent = AgentClass.create(verbose=False)
    task_data = AgentClass.create_task(agent)
    assert isinstance(task_data, dict)
    assert all(key in task_data for key in [
        "description",
        "expected_output",
        "agent"
    ])

@pytest.mark.parametrize("tools", [
    None,
    [MagicMock()],
    [MagicMock(), MagicMock()]
])
def test_agent_creation_with_tools(tools):
    agent = PlannerAgent.create(verbose=False, tools=tools)
    assert isinstance(agent, Agent)
    if tools:
        assert len(agent.tools) == len(tools)

def test_agent_creation_error_handling():
    with patch('crewai.Agent.__init__', side_effect=Exception("Test error")):
        with pytest.raises(Exception):
            PlannerAgent.create()

@pytest.mark.integration
def test_agent_task_chain():
    # Test the complete chain of agents
    planner = PlannerAgent.create(verbose=False)
    writer = WriterAgent.create(verbose=False)
    editor = EditorAgent.create(verbose=False)
    
    # Test task creation and dependencies
    planner_task = PlannerAgent.create_task(planner)
    writer_task = WriterAgent.create_task(writer)
    editor_task = EditorAgent.create_task(editor)
    
    assert all(isinstance(task, dict) for task in [
        planner_task, writer_task, editor_task
    ])

@pytest.mark.parametrize("AgentClass,expected_role", [
    (PlannerAgent, "Content Planner"),
    (WriterAgent, "Content Writer"),
    (EditorAgent, "Editor")
])
def test_agent_roles_and_goals(AgentClass, expected_role):
    agent = AgentClass.create(verbose=False)
    assert agent.role == expected_role
    assert isinstance(agent.goal, str)
    assert isinstance(agent.backstory, str)

def test_agent_task_output_format():
    for AgentClass in [PlannerAgent, WriterAgent, EditorAgent]:
        agent = AgentClass.create(verbose=False)
        task = AgentClass.create_task(agent)
        
        assert "description" in task
        assert isinstance(task["description"], str)
        assert "expected_output" in task
        assert isinstance(task["expected_output"], str)
