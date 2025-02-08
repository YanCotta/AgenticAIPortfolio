# Financial Analysis and Coding with AutoGen

This project demonstrates how to use AutoGen to automate financial analysis and coding tasks, specifically fetching stock data and generating visualizations.

## Prerequisites

-   Python 3.9+ (Recommended)
-   AutoGen
-   yfinance
-   matplotlib
-   python-dotenv
-   pandas

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd AgenticAIPortfolio/AutoGen/FinancialAnalysisAndCoding
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Create a `.env` file in the project root with your OpenAI API key:

    ```
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    ```
    **Important:**  Never commit your `.env` file to version control.  It contains sensitive information.

## Usage

1.  Ensure your OpenAI API key is set up correctly in the `.env` file.
2.  Run the `main.py` script:

    ```bash
    python main.py
    ```

The script will:

1.  Configure the AutoGen agents and the code executor.
2.  Download historical stock prices for NVDA and TSLA.
3.  Generate plots of the stock prices (Year-to-Date).
4.  Save the plots to the `coding` directory.

## Modules

-   `config.py`:  Handles the configuration of the AutoGen agents, code executor, and LLM.  Loads the OpenAI API key securely.
-   `stock_analysis.py`: Contains functions for downloading stock data using `yfinance` and generating stock price plots using `matplotlib`.
-   `main.py`: Orchestrates the entire workflow, initializing the agents, defining tasks, and displaying the results.

## Error Handling

The code includes error handling for:

-   Missing OpenAI API key.
-   Failed stock data retrieval.
-   Empty stock data.
-   Plot saving errors.

## Notes

-   The first time you run the script, AutoGen may download necessary components, which may take a few minutes.
-   The generated plots are saved in the `coding` directory.
-   This project provides a basic example of using AutoGen for financial analysis.  You can extend it to perform more complex tasks, such as analyzing financial statements, predicting stock prices, or building trading strategies.

