"""Configuration management for the LinkedIn Post Generator Agent."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    anthropic_api_key: str
    model_name: str = "claude-sonnet-4-5-20250929"

    # Agent Configuration
    max_iterations: int = 3
    search_queries_count: int = 5

    # Output Settings
    verbose: bool = True
    show_thinking: bool = True

    # Paths
    output_dir: Path = Path("outputs")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
