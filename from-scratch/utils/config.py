from typing import Optional, Dict, Any
import os
from pydantic import BaseModel, Field
from functools import lru_cache
import json
from pathlib import Path

class AppConfig(BaseModel):
    """Application configuration with validation"""
    version: str = Field(default="1.0.0", description="Configuration version")
    openai_api_key: str = Field(default=..., description="OpenAI API key")
    database_url: str = Field(default="sqlite:///default.db", description="Database connection URL")
    debug: bool = Field(default=False, description="Debug mode flag")
    secret_manager: str = Field(default="local", description="Secret management strategy")
    log_level: str = Field(default="INFO", description="Logging level")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout: int = Field(default=30, description="Operation timeout in seconds")

class Config:
    """Configuration manager with hot reload and validation"""
    def __init__(self):
        self._config: Optional[AppConfig] = None
        self._load_config()

    @lru_cache()
    def _load_env_file(self) -> Dict[str, str]:
        """Load environment variables from .env file"""
        env_path = Path(".env")
        if env_path.exists():
            with env_path.open() as f:
                return dict(line.strip().split('=', 1) for line in f if line.strip() and not line.startswith('#'))
        return {}

    def _load_config(self) -> None:
        """Load and validate configuration"""
        env_vars = self._load_env_file()
        for key, value in env_vars.items():
            os.environ.setdefault(key, value)

        self._config = AppConfig(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            database_url=os.getenv("DATABASE_URL", "sqlite:///default.db"),
            debug=os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
            secret_manager=os.getenv("SECRET_MANAGER", "local"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            timeout=int(os.getenv("TIMEOUT", "30"))
        )

    def reload(self) -> None:
        """Hot reload configuration"""
        self._load_env_file.cache_clear()
        self._load_config()

    def get(self, key: str) -> Any:
        """Get configuration value by key"""
        if not self._config:
            self._load_config()
        return getattr(self._config, key)

    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        if not self._config:
            self._load_config()
        return self._config.model_dump()

    def validate(self) -> bool:
        """Validate configuration"""
        try:
            if not self._config:
                self._load_config()
            self._config.model_dump()
            if not self._config.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required")
            return True
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")

# Global config instance
config = Config()

