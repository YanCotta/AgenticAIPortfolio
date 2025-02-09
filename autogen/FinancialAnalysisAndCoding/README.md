# Automated Financial Analysis Using AutoGen Multi-Agent System

## Project Overview
This project demonstrates the implementation of a sophisticated multi-agent system using Microsoft's AutoGen framework to perform automated financial analysis. The system leverages multiple AI agents to collaboratively analyze stock market data, specifically focusing on NVIDIA (NVDA) and Tesla (TSLA) stocks, and generates insightful visualizations.

## Technical Architecture

### Core Components
1. **Multi-Agent System**
   - Code Executor Agent: Handles code execution and environment interactions **(Dockerized)**
   - Code Writer Agent: Generates and optimizes analysis code
   - **Analysis Agent: Performs advanced stock analysis using plugins**
   - Both agents communicate via AutoGen's conversation protocols

2. **Key Modules**
   - `stock_analysis.py`: Core financial data processing and visualization
   - `config.py`: Agent configuration and system settings management
   - `main.py`: Orchestration and workflow management
   - `logger.py`: Comprehensive logging system using Loguru
   - `utils.py`: Environmental configuration and utility functions

3. **Testing Infrastructure**
   - Comprehensive test suite using pytest
   - Mock implementations for external services
   - Coverage for both unit and integration tests

## Technical Requirements

### System Requirements
- Python 3.9 or higher
- Git for version control
- Unix-based OS recommended (Linux/macOS), Windows supported

### Key Dependencies
- AutoGen: Multi-agent orchestration
- yfinance: Financial data retrieval
- pandas: Data manipulation
- matplotlib: Data visualization
- python-dotenv: Environment management
- pydantic: Data validation
- loguru: Advanced logging

## Installation & Setup

1. **Clone Repository**
   ```bash
   git clone <repository_url>
   cd AgenticAIPortfolio/AutoGen/FinancialAnalysisAndCoding
   ```

2. **Virtual Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix-based systems
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file with:
   OPENAI_API_KEY=your_api_key_here
   ```

## Project Structure

```
MultiAgentFinancialAnalysis/
├── MultiAgentFinancialAnalysis/
│   ├── __init__.py
│   ├── config.py          # System configuration
│   ├── logger.py          # Logging setup
│   ├── main.py           # Application entry point
│   ├── stock_analysis.py  # Financial analysis logic
│   └── utils.py          # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Test configurations
│   ├── test_multiagent.py
│   └── test_stock_analysis.py
├── logs/                 # Generated log files
└── coding/              # Generated visualizations
```

## Implementation Details

### Agent Configuration
- Utilizes AutoGen's ConversableAgent and AssistantAgent
- Custom code executor configuration for secure code execution **using Docker**
- **AnalysisAgent with plugin architecture for incorporating additional factors**
- Robust error handling and logging

### Financial Analysis Features
- Real-time stock data retrieval
- YTD price analysis for NVDA and TSLA
- Automated visualization generation
- Comparative stock performance analysis

### Data Visualization
- Stock price trends
- YTD gains comparison
- Interactive matplotlib plots
- Automated save functionality

## Usage Examples

1. **Basic Usage**
   ```bash
   python -m MultiAgentFinancialAnalysis.main
   ```

2. **Output**
   - Generates two visualization files:
     - `ytd_stock_gains.png`: Year-to-Date gains comparison
     - `stock_prices_YTD_plot.png`: Price trend analysis

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=MultiAgentFinancialAnalysis
```

## Error Handling & Logging

The system implements comprehensive error handling for:
- API authentication failures
- Data retrieval issues
- File I/O operations
- Agent communication errors

Logs are:
- Automatically rotated at 10MB
- Retained for one week
- Compressed for storage efficiency
- Thread-safe for concurrent operations

## Future Enhancements
- Additional financial indicators
- Extended historical analysis
- Portfolio optimization features
- Real-time market alerts
- Enhanced visualization options
- **Expanded plugin ecosystem for the AnalysisAgent**
- Enhanced security through improved containerization

## License
MIT license.