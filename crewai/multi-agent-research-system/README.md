# 🤖 Multi-Agent Research & Content Creation System

A sophisticated AI-powered research and content creation platform leveraging CrewAI's multi-agent architecture to automate and enhance content production through collaborative artificial intelligence.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-0.28.8-orange)
![Tests](https://img.shields.io/badge/tests-passing-green)

## 🎯 System Architecture

### Core Agents

1. **Planning Agent** (`src/agents/planner.py`)
   - Content strategy development
   - Topic research coordination
   - SEO keyword analysis
   - Audience targeting

2. **Writing Agent** (`src/agents/writer.py`)
   - Content generation
   - SEO optimization
   - Structure implementation
   - Markdown formatting

3. **Editing Agent** (`src/agents/editor.py`)
   - Quality assurance
   - Technical accuracy verification
   - Style consistency
   - Final polishing
   - Deep investigation capability (if requested)

### Support Systems

- **Utility Module** (`src/utils/helpers.py`)
  - Environment management
  - API key handling
  - Text formatting
  - Error logging
- **Research Storage** (`src/research_storage.py`)
  - FAISS-based vector database for efficient research data retrieval.

## 🛠 Technical Stack

- **Framework**: CrewAI 0.28.8
- **Language**: Python 3.8+
- **Dependencies**:
  - crewai_tools==0.1.6
  - langchain_community==0.0.29
  - pydantic>=2.0.0
  - python-dotenv>=0.19.0
  - faiss-cpu

## 📦 Project Structure

```
MultiAgentResearchSystem/
├── src/
│   ├── agents/                 # Agent definitions
│   │   ├── planner.py         # Content planning agent
│   │   ├── writer.py          # Content writing agent
│   │   └── editor.py          # Content editing agent
│   ├── utils/
│   │   └── helpers.py         # Utility functions
│   ├── research_storage.py    # Research storage module
│   └── main.py               # System orchestration
├── tests/                    # Comprehensive test suite
│   ├── test_agents.py       # Agent functionality tests
│   ├── test_utils.py        # Utility function tests
│   ├── test_content_system.py # Integration tests
│   └── test_performance.py  # Performance tests
└── requirements.txt         # Project dependencies
```

## 🚀 Installation

1. Clone the repository:

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
# Create .env file with:
OPENAI_API_KEY=your_openai_api_key
```

## 💻 Usage Example

```python
from src.main import ContentCreationSystem

# Initialize system
system = ContentCreationSystem()

# Generate content
result = system.generate_content(
    topic="Artificial Intelligence in Healthcare"
)
print(result)
```

## 🔍 Key Features

### Intelligent Content Planning
- Topic analysis
- Audience targeting
- SEO strategy
- Content structuring

### Advanced Content Generation
- Research-based writing
- SEO optimization
- Markdown formatting
- Citation management

### Quality Assurance
- Technical accuracy checks
- Style consistency
- Grammar verification
- Content flow optimization

## 🔄 Process Flow

1. Content Planning Phase
   ```python
   planner = PlannerAgent.create()
   plan = planner.execute(topic)
   ```

2. Content Writing Phase
   ```python
   writer = WriterAgent.create()
   content = writer.execute(plan)
   ```

3. Content Editing Phase
   ```python
   editor = EditorAgent.create()
   final_content = editor.execute(content)
   ```

## 🧪 Testing

The system includes comprehensive testing:

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_agents.py
pytest tests/test_utils.py
pytest tests/test_content_system.py
pytest tests/test_performance.py
```

## 📊 Output Format

```python
{
    "content": {
        "title": str,
        "sections": List[Dict],
        "references": List[str]
    },
    "metadata": {
        "word_count": int,
        "reading_time": str,
        "seo_score": float
    }
}
```

## ⚙️ Configuration

### Agent Configuration
```python
AGENT_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1500
}
```

### Research Configuration
```python
RESEARCH_CONFIG = {
    "MAX_RESEARCH_DEPTH": 5
}
```

## 🚀 Production Considerations

- Implement rate limiting
- Add result caching
- Set up monitoring
- Configure error handling
- Implement backup strategies

## 🔬 Development Features

This project demonstrates expertise in:
- Multi-agent system architecture
- Natural Language Processing
- Test-Driven Development
- Error handling
- Configuration management
- Documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.