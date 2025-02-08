from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo"
    MAX_RETRIES: int = 3
    MAX_RESEARCH_RESULTS: int = 2
    
    class Config:
        env_file = ".env"