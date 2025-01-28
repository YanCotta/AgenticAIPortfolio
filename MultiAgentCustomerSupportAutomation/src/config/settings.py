import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

OPENAI_MODEL = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1500
}

COMPANY_INFO = {
    "name": "YourCompany",
    "docs_url": "https://docs.yourcompany.com",
    "support_email": "support@yourcompany.com"
}

LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
