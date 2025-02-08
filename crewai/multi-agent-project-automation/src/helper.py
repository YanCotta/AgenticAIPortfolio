# Add your utilities or helper functions to this file.

import os
from dotenv import load_dotenv, find_dotenv

def load_env() -> None:
    """
    Loads environment variables from the .env file.
    
    Raises:
        FileNotFoundError: if the .env file is not found.
    """
    load_dotenv(find_dotenv())

def get_openai_api_key() -> str:
    """
    Retrieves the OpenAI API key from environment variables.
    
    Returns:
        str: The OpenAI API key.
        
    Raises:
        EnvironmentError: If the API key is not found.
    """
    load_env()
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError("Missing OPENAI_API_KEY in environment variables")
    return key
