from typing import Optional, List
import os
import logging
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_env() -> None:
    """Load environment variables from .env file."""
    try:
        if not load_dotenv(find_dotenv()):
            raise EnvironmentError("No .env file found")
        logger.info("Environment variables loaded successfully")
    except Exception as e:
        logger.error(f"Error loading environment variables: {e}")
        raise

def get_api_key(key_name: str) -> Optional[str]:
    """Retrieve API key from environment variables."""
    try:
        load_env()
        api_key = os.getenv(key_name)
        if not api_key:
            logger.warning(f"{key_name} not found in environment variables")
            return None
        return api_key
    except Exception as e:
        logger.error(f"Error retrieving {key_name}: {e}")
        return None

def pretty_print_result(text: str, max_length: int = 80) -> str:
    """Format text with line breaks at appropriate positions."""
    try:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
            
        lines: List[str] = []
        for line in text.split('\n'):
            if len(line) <= max_length:
                lines.append(line)
                continue

            current_line = ''
            for word in line.split(' '):
                if len(current_line) + len(word) + 1 <= max_length:
                    current_line = f"{current_line} {word}".strip()
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

        return '\n'.join(lines)
    except Exception as e:
        logger.error(f"Error formatting text: {e}")
        return text
