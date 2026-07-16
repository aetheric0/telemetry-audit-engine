
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PROJECT_NAME: str| None = None

    # ChromaDB persistence path
    CHROMA_PERSIST_DIR: str | Path = ""

    # Static API key for node authentication
    API_KEY: str | None = None

    # LLM Provider Config
    LLM_API_KEYS: list[str] | None = None

    GROQ_API_KEY: str | None = None

    # Logging Config
    LOG_FILE: str | None = None


settings = Settings()