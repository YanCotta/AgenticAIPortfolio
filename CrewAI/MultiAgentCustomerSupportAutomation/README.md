# Multi-Agent Customer Support Automation

An intelligent customer support automation system built with CrewAI that leverages multiple AI agents to provide comprehensive and accurate customer support. This project uses the CrewAI framework as its main tool for development.

## Features

- 🤖 Multiple specialized AI agents working in coordination
- 📚 Automated documentation search and reference
- ✅ Quality assurance checks on responses
- 🔄 Retry mechanism for robust operation
- 📝 Comprehensive logging system
- 🛡️ Type-safe implementation

## System Architecture

The system consists of two main agents:
1. **Support Agent**: Handles primary customer inquiries and documentation searches
2. **QA Agent**: Verifies response accuracy and completeness

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Serper API key (for documentation search)
- CrewAI Framework 

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MultiAgentCustomerSupportAutomation.git
cd MultiAgentCustomerSupportAutomation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
LOG_LEVEL=INFO
```

## Usage

Basic usage example:

```python
from src.main import CustomerSupportSystem

# Initialize the system
support_system = CustomerSupportSystem()

# Handle a customer inquiry
result = support_system.handle_inquiry(
    customer_info={"name": "John Doe", "id": "12345"},
    inquiry="How do I reset my password?"
)

print(result)
```

## Configuration

Customize the system behavior in `src/config/settings.py`:

- Modify `COMPANY_INFO` with your company details
- Adjust `OPENAI_MODEL` parameters
- Configure logging settings

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
```

4. Run linter:
```bash
flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewai) for the multi-agent framework
- OpenAI for the language model capabilities
