# Multi-Agent Content Creation System

An intelligent content creation pipeline using multiple AI agents to generate, analyze, and optimize content at scale.

## 🌟 Features

- Automated market research and analysis
- Data-driven content generation
- Multi-platform social media post creation
- Quality assurance and content optimization
- Markdown-formatted output
- Configurable agent roles and tasks

## 🛠 Prerequisites

- Python 3.9+
- OpenAI API key
- Groq API key (optional, for alternative LLM)
- Serper API key (for web search capabilities)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MultiAgentContentCreation.git
cd MultiAgentContentCreation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
GROQ_API_KEY=your_groq_api_key
```

## 🚀 Usage

Run the main script:
```bash
python src/main.py
```

## 📁 Project Structure

```
MultiAgentContentCreation/
├── config/
│   ├── agents.yaml     # Agent configurations
│   └── tasks.yaml      # Task definitions
├── src/
│   ├── agents.py       # Agent and crew setup
│   ├── main.py         # Main execution script
│   ├── models.py       # Data models
│   └── helper.py       # Utility functions
├── requirements.txt
└── README.md
```

## ⚙️ Configuration

Modify `config/agents.yaml` and `config/tasks.yaml` to adjust agent behaviors and task parameters.

## 📄 Output

The system generates:
- Markdown-formatted articles
- Platform-specific social media posts
- Detailed market analysis
- Quality-assured content

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.