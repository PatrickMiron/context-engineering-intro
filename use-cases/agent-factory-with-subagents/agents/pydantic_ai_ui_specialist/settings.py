"""
Pydantic AI UI Specialist Agent Configuration

Handles environment variables and settings for the UI/UX specialist agent.
"""

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for the LLM provider")
    llm_model: str = Field(default="gpt-4", description="Model name to use")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1", description="Base URL for the LLM API"
    )

    # Agent Configuration
    agent_name: str = Field(
        default="UI Specialist", description="Name of the UI/UX specialist agent"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for failed operations"
    )


def load_settings() -> Settings:
    """
    Load settings with proper error handling and environment loading.

    Returns:
        Settings: Loaded settings instance

    Raises:
        ValueError: If required settings are missing or invalid
    """
    # Load environment variables from .env file
    load_dotenv()

    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nMake sure to set LLM_API_KEY in your .env file"
        raise ValueError(error_msg) from e


def get_llm_model():
    """
    Get configured LLM model with proper environment loading.

    Returns:
        OpenAIModel: Configured LLM model instance
    """
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url, api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
