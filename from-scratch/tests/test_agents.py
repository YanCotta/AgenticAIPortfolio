import asyncio
import time
import random
import string
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

# Import agents and orchestrator components
from agents.summarizer_agent import SummarizerAgent
from agents.email_agent import EmailAgent
from orchestrator.task_manager import TaskManager
from agents.doc_ingest_agent import DocumentIngestionAgent
from agents.task_router_agent import TaskRouterAgent

# Dummy ingestion agent for integration tests
class DummyIngestionAgent:
    def process(self, file_path):
        return {
            "text": "This is a sample text for summarization.",
            "metadata": {"file_name": file_path, "recipient": "test@example.com"}
        }

# Test data generator for random inputs
def generate_test_data(num_chars=100):
    text = ''.join(random.choices(string.ascii_letters + " ", k=num_chars))
    metadata = {"file_name": "test.txt", "recipient": "test@example.com"}
    return {"text": text, "metadata": metadata}

# Unit test: DocumentIngestionAgent
def test_doc_ingest_agent():
    agent = DocumentIngestionAgent()
    result = agent.process("tests/sample.txt")
    assert "text" in result and "metadata" in result, "Document ingestion failed"
    assert len(result["text"]) > 0, "Extracted text should not be empty"

# Unit test: TaskRouterAgent
@pytest.mark.asyncio
async def test_task_router_agent():
    agent = TaskRouterAgent()
    result = await agent.process("tests/sample.txt")
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "document" in result and "summary" in result, "Task routing failed"

# Integration test: Run end-to-end pipeline using a dummy ingestion agent
@pytest.mark.asyncio
async def test_pipeline_integration(monkeypatch):
    tm = TaskManager()
    tm.ingestion_agent = DummyIngestionAgent()  # Inject dummy ingestion
    result = await tm.execute_pipeline("dummy_file.txt", priority=3)
    assert result is not None, "Pipeline execution failed"

# Performance test: Verify summarizer performance under threshold
@pytest.mark.asyncio
async def test_summarizer_performance():
    agent = SummarizerAgent()
    test_input = generate_test_data()
    start = time.time()
    result = await agent.process(test_input)
    elapsed = time.time() - start
    assert result is not None, "Summarizer failed"
    # Increased threshold to 15 seconds to account for API latency
    assert elapsed < 15, f"Performance issue: {elapsed:.2f}s elapsed"

# Load test: Run multiple summarization tasks concurrently
@pytest.mark.asyncio
async def test_load_summarizer():
    agent = SummarizerAgent()
    tasks = [agent.process(generate_test_data()) for _ in range(5)]  # Reduced to 5 concurrent tasks
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for res in results:
        assert not isinstance(res, Exception), f"Task failed with: {res}"
        assert res is not None, "One summarization task failed under load"

# Chaos test: Inject errors into OpenAI calls
@pytest.mark.asyncio
async def test_chaos_summarizer(monkeypatch):
    agent = SummarizerAgent()
    async def chaotic_create(*args, **kwargs):
        raise Exception("Injected chaos error")
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = chaotic_create
    monkeypatch.setattr(agent, "client", mock_client)
    
    test_input = generate_test_data()
    result = await agent.process(test_input)
    assert result is not None, "Should return result object even on failure"
    assert result["summary"] is None, "Summary should be None on failure"

# EmailAgent test: Validate email processing and HTML output
def test_email_agent():
    agent = EmailAgent()
    test_data = {
        "summary": "This is a test summary.",
        "metadata": {"file_name": "report.pdf", "recipient": "test@example.com"},
        "html": True
    }
    result = agent.process(test_data)
    assert "subject" in result and "body" in result, "Email agent output is incomplete"
    assert "<html>" in result["body"], "HTML email format not generated"

# Mocking external API calls for deterministic tests
@pytest.mark.asyncio
async def test_summarizer_with_mock(monkeypatch):
    agent = SummarizerAgent()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mocked summary"))]
    mock_response.usage = MagicMock(total_tokens=100)
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(agent, "client", mock_client)
    
    test_input = generate_test_data()
    result = await agent.process(test_input)
    assert result["summary"] == "Mocked summary", "Mocking failed"
