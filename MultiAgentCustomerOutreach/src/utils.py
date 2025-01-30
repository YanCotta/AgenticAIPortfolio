import os
from dotenv import load_dotenv, find_dotenv

def load_env() -> None:
    """Load environment variables from a .env file."""
    _ = load_dotenv(find_dotenv())

def get_openai_api_key() -> str:
    """Retrieve the OpenAI API key from environment variables."""
    load_env()
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not set in environment")
    return key

def get_serper_api_key() -> str:
    """Retrieve the Serper API key from environment variables."""
    load_env()
    key = os.getenv("SERPER_API_KEY")
    if not key:
        raise ValueError("SERPER_API_KEY is not set in environment")
    return key

def pretty_print_result(result: str) -> str:
    """
    Format the result by breaking lines longer than 80 characters without splitting words.
    
    Args:
        result (str): The string to be formatted.
        
    Returns:
        str: The formatted string.
    """
    parsed_result = []
    for line in result.split('\n'):
        if len(line) > 80:
            words = line.split(' ')
            new_line = ''
            for word in words:
                if len(new_line) + len(word) + 1 > 80:
                    parsed_result.append(new_line)
                    new_line = word
                else:
                    new_line = f"{new_line} {word}".strip()
            parsed_result.append(new_line)
        else:
            parsed_result.append(line)
    return "\n".join(parsed_result)
