"""Configuration management using Pydantic."""

import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings(BaseModel):
    """Settings for the financial analysis application."""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY", description="OpenAI API key")
    log_level: str = Field("INFO", env="LOG_LEVEL", description="Logging level")
    timeout: int = Field(60, env="TIMEOUT", description="Timeout for API calls")
    work_dir: str = Field("coding", env="WORK_DIR", description="Working directory for code execution")

    class Config:
        """Configuration settings for Pydantic."""
        env_file = ".env"
        env_nested_delimiter = "__"

def get_settings() -> Settings:
    """
    Retrieves the settings for the financial analysis application.

    Returns:
        Settings: An instance of the Settings class containing the application settings.
    """
    return Settings()

settings = get_settings()
