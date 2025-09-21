# Application configuration and environment variables
# TODO: Implement settings management with Pydantic

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # LLM Configuration
    default_llm_provider: str = "ollama"
    default_llm_model: str = "llama2"
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # LangSmith Configuration
    langsmith_tracing: bool = False
    langchain_endpoint: Optional[str] = None
    langchain_api_key: Optional[str] = None
    langchain_project: Optional[str] = None
    
    # SSLCommerz Configuration
    sslcommerz_store_id: str = ""
    sslcommerz_store_password: str = ""
    sslcommerz_is_sandbox: bool = True
    
    # Security
    jwt_secret_key: str = "your-secret-key-here"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Application
    evaluation_price_bdt: int = 50
    free_trial_credits: int = 3
    max_word_count: int = 400
    min_word_count: int = 150
    
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra environment variables like LangChain settings
    )

settings = Settings()
