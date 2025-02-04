# MultiAgentProjectAutomation

An intelligent project management automation system powered by CrewAI that leverages multiple AI agents to plan, estimate, and allocate resources for projects.

## Features

- 🤖 Multi-agent collaboration using CrewAI framework
- 📊 Automated project task breakdown and planning
- ⏱️ Intelligent time and resource estimation
- 📋 Strategic resource allocation
- 🔄 Pydantic models for data validation
- ⚙️ YAML-based configuration for agents and tasks

## Prerequisites

- Python 3.9.6 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MultiAgentProjectAutomation.git
cd MultiAgentProjectAutomation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
MultiAgentProjectAutomation/
├── src/
│   ├── agents.py         # Agent definitions and configuration
│   ├── helper.py         # Utility functions
│   ├── main.py          # Main application logic
│   └── models.py        # Pydantic data models
├── config/
│   ├── agents.yaml      # Agent configurations
│   └── tasks.yaml       # Task configurations
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Usage

```python
from src.main import run_project_planning, format_project_inputs

# Format your project inputs
project_inputs = format_project_inputs(
    project="Website",
    objectives="Create a website for a small business",
    industry="Technology",
    team_members="""
    - John Doe (Project Manager)
    - Jane Doe (Software Engineer)
    - Bob Smith (Designer)
    """,
    requirements="""
    - Create a responsive design
    - Implement modern UI
    - Develop user-friendly navigation
    """
)

# Run the project planning
result, metrics = run_project_planning(project_inputs)
print(result)
```

## Configuration

The system uses YAML configuration files for both agents and tasks. You can customize the behavior by modifying:

- `config/agents.yaml`: Define agent roles, goals, and backstories
- `config/tasks.yaml`: Configure task descriptions and expected outputs

## Models

The system uses Pydantic models for data validation:

- `TaskEstimate`: Represents individual task estimates
- `Milestone`: Represents project milestones
- `ProjectPlan`: Represents the complete project plan

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- OpenAI for the GPT models
