from __future__ import annotations

from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices


class Settings(BaseSettings):
    # LLM provider selection and defaults
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")

    # OpenAI
    # Prefer user-provided env var; fall back to standard name
    openai_api_key: str | None = Field(default=None, validation_alias=AliasChoices("CONFRADAR_SA_OPENAI", "OPENAI_API_KEY"))
    # Base URL for OpenAI-compatible API; prefer LiteLLM proxy if provided
    openai_base_url: str = Field(
        default="http://localhost:4000",
        validation_alias=AliasChoices("LITELLM_BASE_URL", "LLM_BASE_URL", "OPENAI_BASE_URL"),
    )
    # Database connection URL; default to PostgreSQL (use SQLite for local testing: sqlite:///confradar.db)
    database_url: str = Field(default="postgresql+psycopg://confradar:confradar@localhost:5432/confradar", alias="DATABASE_URL")
    openai_timeout_s: float = Field(default=20.0, alias="OPENAI_TIMEOUT_S")
    openai_max_retries: int = Field(default=3, alias="OPENAI_MAX_RETRIES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()  # Loaded at import-time for convenience in small apps


def get_settings() -> Settings:
    """Get application settings.
    
    Returns:
        Settings instance
    """
    return settings
