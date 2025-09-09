from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Emergency Accident Response System"
    API_V1_PREFIX: str = "/v1"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # Google Maps Configuration  
    GOOGLE_MAPS_API_KEY: str
    
    # Twilio Configuration
    ACCOUNT_SID: str
    AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    
    # Model Configuration
    OLLAMA_MODEL: str = 'gpt-oss:20b'
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Backward compatibility
OLLAMA_MODEL = settings.OLLAMA_MODEL