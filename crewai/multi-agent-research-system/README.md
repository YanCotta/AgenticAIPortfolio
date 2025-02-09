<div align="center">

# 🤖 Multi-Agent Research & Content Creation System

> A sophisticated AI-powered research and content creation platform leveraging CrewAI's multi-agent architecture.

[![Python](https://img.shields.io/badge/Python-3.8+-4584b6?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.28.8-FF6B6B?style=for-the-badge&logo=robot&logoColor=white)](https://github.com/joaomdmoura/crewAI)
[![Tests](https://img.shields.io/badge/Tests-Passing-2EA44F?style=for-the-badge&logo=github)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📑 Quick Links
- [System Architecture](#-system-architecture)
- [Technical Stack](#-technical-stack)
- [Installation](#-installation)
- [Usage Example](#-usage-example)
- [Key Features](#-key-features)
- [Testing](#-testing)
- [Contributing](#-contributing)

---

## 🎯 System Architecture

### 🤖 Core Agents

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

### 🛠 Support Systems

- **Utility Module** (`src/utils/helpers.py`)
  - Environment management
  - API key handling
  - Text formatting
  - Error logging
- **Research Storage** (`src/research_storage.py`)
  - FAISS-based vector database for efficient research data retrieval.

---

## 💻 Technical Stack

<div align="center">

| Technology | Version | Purpose |
|------------|---------|----------|
| CrewAI | 0.28.8 | Multi-agent Framework |
| Python | 3.8+ | Core Language |
| crewai_tools | 0.1.6 | Agent Utilities |
| langchain_community | 0.0.29 | LLM Integration |
| FAISS | Latest | Vector Database |

</div>

## 📦 Project Structure

<details>
<summary>Click to expand project tree</summary>

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

</details>

---

## 🚀 Installation

<details>
<summary>Step-by-step guide</summary>

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

</details>

---

## 💻 Usage Example

<details>
<summary>View example code</summary>

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

</details>

---

## 🔍 Key Features

<div align="center">

| Feature | Description |
|---------|-------------|
| 🎯 Intelligent Planning | Topic analysis, SEO strategy, audience targeting |
| ✍️ Advanced Generation | Research-based writing, SEO optimization |
| 🔎 Quality Assurance | Technical accuracy, style consistency |

</div>

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

---

## 🔄 Process Flow

<div align="center">

```mermaid
graph LR
    A[Planning Agent] --> B[Writing Agent]
    B --> C[Editing Agent]
    C --> D[Final Content]
    style A fill:#ff9900
    style B fill:#00b4d8
    style C fill:#2ea44f
    style D fill:#6f42c1
```

</div>

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

---

## 🧪 Testing

<details>
<summary>View testing instructions</summary>

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

</details>

---

## ⚙️ Configuration

<details>
<summary>View configuration details</summary>

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

</details>

---

## 🚀 Production Considerations

<div align="center">

| Consideration | Implementation |
|---------------|----------------|
| Rate Limiting | ⚡️ Request throttling |
| Caching | 💾 Result storage |
| Monitoring | 📊 System metrics |
| Error Handling | 🛡️ Robust recovery |
| Backup | 💽 Data protection |

</div>

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

---

<div align="center">

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red.svg?style=for-the-badge" alt="Made with love">

</div>