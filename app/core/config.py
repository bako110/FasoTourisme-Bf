from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuration de l'application Tourisme Burkina"""
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "tourisme_burkina"
    
    # Application
    APP_NAME: str = "Tourisme Burkina API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Sécurité & JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-please-do-it-now"
    
    # CORS - peut être une chaîne séparée par des virgules ou une liste JSON
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080,http://192.168.11.157:8000,*"
    
    @property
    def cors_origins(self) -> list:
        """Convertit ALLOWED_ORIGINS en liste"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return self.ALLOWED_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
