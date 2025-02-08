"""Utilities or helper functions."""

import os
from dotenv import load_dotenv, find_dotenv
from financial_analysis.logger import get_logger

logger = get_logger(__name__)

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService
def load_env():
    """Loads environment variables from a .env file."""
    _ = load_dotenv(find_dotenv())

def get_openai_api_key() -> str:
    """
    Retrieves the OpenAI API key from the environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OPENAI_API_KEY not found in environment variables.")
    return openai_api_key
