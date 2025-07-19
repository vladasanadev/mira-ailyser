"""
Configuration settings for Weaviate connection
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class WeaviateConfig(BaseSettings):
    """Weaviate configuration settings"""
    
    # Weaviate Cloud connection settings
    weaviate_url: str
    weaviate_api_key: str
    
    # Optional inference API keys
    openai_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    
    # Connection settings
    timeout_config: int = 120  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global config instance
config = WeaviateConfig() 