from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    MODEL_NAME: str = "gpt-3.5-turbo"
    DATABASE_URL: str = "sqlite:///./database.db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
+   TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY")
