import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    app_name: str = "Healthcare Chatbot API"
    debug: bool = False
    environment: str = "development"
    
    # Database Settings
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "user"
    db_password: str = "pass"
    db_name: str = "tasksdb"
    
    # Security Settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI/Gemini Settings
    gemini_api_key: str = "AIzaSyB3cVJYlPCmUkIgQSXzSNRYiggSt6E-mc0"
    gemini_model: str = "gemini-2.0-flash-exp"
    
    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001"
    
    @property
    def cors_origins(self) -> list:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    @property
    def database_url(self) -> str:
        """Generate database URL from components"""
        return f"mariadb+mariadbconnector://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()
