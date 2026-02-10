import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application
    APP_NAME: str = "Secon E-book Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./ebook.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # API Keys
    HUGGINGFACE_API_KEY: str = ""
    UNSPLASH_ACCESS_KEY: str = ""
    GOOGLE_BOOKS_API_KEY: str = ""
    RAPIDAPI_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # File Upload
    MAX_FILE_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx", "txt", "md", "html", "epub"]
    TEMP_DIR: str = "/tmp/ebook_temp"
    OUTPUT_DIR: str = "./generated_ebooks"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # N8N
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
