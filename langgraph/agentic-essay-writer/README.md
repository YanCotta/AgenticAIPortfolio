# 📝 Agentic Essay Writer

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Powered-orange.svg)](https://github.com/langchain-ai/langgraph)

> A sophisticated AI-powered essay generation system leveraging LangGraph for agent orchestration and multi-step reasoning.

## 🎯 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-essay-writer.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/ui/gradio_app.py
```

## 🌟 Project Overview

The Agentic Essay Writer employs multiple specialized AI agents working in concert to generate high-quality essays through a series of coordinated steps:

🔹 **Planning** - Structures the essay's core arguments and outline
🔹 **Research** - Gathers relevant information using Tavily's search API
🔹 **Writing** - Composes the essay based on the plan and research
🔹 **Critique** - Reviews and suggests improvements

## 🏗️ Architecture

```plaintext
src/
├── agents/              # Specialized AI agents
│   ├── planner.py      # Essay structure and outline generation
│   ├── researcher.py   # Information gathering using Tavily
│   ├── writer.py       # Essay composition
│   └── critic.py       # Quality assessment and feedback
├── controller/          # Orchestration logic
│   └── essay_controller.py
├── models/             # Data models and schemas
│   └── schema.py
├── services/           # External service integrations
│   └── research_service.py
├── ui/                 # User interface
│   └── gradio_app.py
├── utils/             # Shared utilities
│   ├── logging.py
│   ├── state.py
│   └── validation.py
└── workflow/          # Business logic
    └── essay_workflow.py
```

## ✨ Key Features

### 🤖 Agent System

- Modular Agent Architecture: Each agent (Planner, Researcher, Writer, Critic) operates independently with clear responsibilities
- State Management: Robust state tracking across the essay generation pipeline
- Error Handling: Comprehensive error handling and logging throughout the agent system

### 🛠️ Technical Implementation

- Async/Await Pattern: Leverages Python's asynchronous capabilities for efficient operations
- Type Safety: Comprehensive type hints and Pydantic models for data validation
- Dependency Injection: Clean separation of concerns and testable components

### 🖥️ User Interface

- Interactive Gradio UI: Real-time essay generation and editing
- State Visualization: Track the progress and state of the essay generation
- Multi-threaded Support: Handle multiple essay generation processes simultaneously

## 🚀 Installation
- Clone the repository
- Install dependencies 
- Configure environment variables
- Run the application 

## 📘 Usage 

### 📝 Starting an Essay:
Enter your essay topic in the input field
Click "Generate Essay" to begin the process
The system will execute the full pipeline: Plan → Research → Write → Critique

### 📊 Monitoring Progress:
Track the current agent and state in the "Agent" tab
View detailed state history in "StateSnapshots"
Monitor research content and intermediate outputs

### ✏️ Editing and Refinement:
Modify the plan, draft, or critique directly in their respective tabs
Continue the generation process with modifications
Track revision history and agent interactions

## 🔧 Technical Details

### State Management
- **AgentState**: Core data model tracking essay progress  
- **StateManager**: Handles state transitions and persistence  
- **EssayController**: Orchestrates agent interactions and state updates  

### Agent Communication
- Asynchronous message passing between agents  
- Structured prompt templates for consistent agent behavior  
- Error recovery and retry mechanisms  

### Testing
- Comprehensive unit tests for each agent  
- Integration tests for the full workflow  
- Mock services for deterministic testing  

## 👨‍💻 Development

### Running Tests

### Adding New Agents
1. Implement the `BaseAgent` abstract class  
2. Add configuration in `config.py`  
3. Register the agent in `EssayWorkflow`  
4. Update tests accordingly  

## 🔮 Future Enhancements
- [ ] Advanced research capabilities (multi-source validation)  
- [ ] Enhanced critique with specific improvement suggestions  
- [ ] Support for different essay styles and formats  
- [ ] Performance optimization for longer essays  
- [ ] Integration with additional LLM providers  

## 🤝 Contributing

<details>
<summary>Click to expand contributing guidelines</summary>

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request  

</details>

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  

## 🙏 Acknowledgments
- [**LangGraph**](https://github.com/langchain-ai/langgraph) for the agent orchestration framework  
- [**Tavily**](https://tavily.com) for research capabilities  
- [**OpenAI**](https://openai.com) for language model access

---

<div align="center">
Made with ❤️ by the Agentic Essay Writer Team
</div>