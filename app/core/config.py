import secrets
from pydantic import (AnyUrl)
from typing import Literal, Any
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[AnyUrl] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',') if i.strip()]
    if isinstance(v, str) and v.startswith('['):
        import json
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return [str(i).strip() for i in parsed]
            return str(parsed)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format for CORS origin {v}")
    if isinstance(v, list):
        return v
    raise ValueError("")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 * 24 * 6 = 6 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 6
    FRONTEND_HOST="http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PROJECT_NAME: str

settings = Settings()