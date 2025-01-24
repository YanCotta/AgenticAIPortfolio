# MultiAgentResearchSystem

A sophisticated system designed to automate research and content creation tasks using AI-Agents and Multi-AI-Agents.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://github.com/yourusername/AgenticAIPortfolio/workflows/tests/badge.svg)

## Project Structure
```
MultiAgentResearchSystem/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── writer.py
│   │   └── editor.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_utils.py
├── data/
│   └── output/
├── docs/
│   └── API.md
├── .env.example
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

## Overview
The MultiAgentResearchSystem leverages the crewAI framework to define and manage multiple AI agents, each with specific roles and goals. These agents collaborate to perform complex tasks such as researching topics, writing articles, and editing content, thereby streamlining the content creation process.

## Features
- Multi-agent collaboration system using crewAI framework
- Role-specific agents: Planner, Writer, and Editor
- Automated content research and generation
- Configurable agent behaviors and goals
- Robust error handling and logging
- Comprehensive test coverage

## Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/AgenticAIPortfolio.git
    cd AgenticAIPortfolio/MultiAgentResearchSystem
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your-openai-api-key
    SERPER_API_KEY=your-serper-api-key
    ```

## Usage
Run the `research_agents_crew.py` script to see the agents in action:
```bash
python research_agents_crew.py
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 guidelines. Format your code using:
```bash
black src/ tests/
```

### Type Checking
```bash
mypy src/
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.
