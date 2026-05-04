"""Configuration management for the Text Summarizer application"""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file"""
    
    # Application
    app_name: str = "Text Summarizer API"
    app_description: str = "AI-powered text summarization using Hugging Face T5"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    
    # Model
    model_path: str = "./models/saved_summary_model"
    device: str = "auto"  # auto, cpu, cuda, mps
    
    # Summarization
    max_input_length: int = 512
    max_output_length: int = 150
    num_beams: int = 4
    early_stopping: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
