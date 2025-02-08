
# Agentic Essay Writer

An AI-powered essay writing tool that leverages LangGraph for agent orchestration.

## Setup

1.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
2.  Create a `.env` file based on the `.env.example` file and fill in the necessary API keys:

    ```bash
    cp .env.example .env
    # Edit .env and add your API keys
    ```
3.  Run the application:

    ```bash
    python -m src.main
    ```

## Features

*   AI-powered essay generation
*   Agent orchestration using LangGraph
*   Modular design for easy extension
*   Gradio UI for interactive usage

## Next Steps

*   Implement a more sophisticated state management system.
*   Add more agents for different tasks (e.g., fact-checking, grammar correction).
*   Improve the UI with more features and customization options.
*   Add more comprehensive tests.
