"""
Configuration settings for the Emergency Response AI System
"""
import os

class Settings:
    """Application settings from environment variables"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # Application Settings
    PROJECT_NAME: str = "Emergency Response AI System"
    APP_NAME: str = "Emergency Response AI System"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Cost Protection Settings
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"  # Default to demo mode
    MAX_DAILY_OPENAI_REQUESTS: int = int(os.getenv("MAX_DAILY_OPENAI_REQUESTS", "50"))
    MAX_DAILY_GOOGLE_REQUESTS: int = int(os.getenv("MAX_DAILY_GOOGLE_REQUESTS", "100"))
    MAX_DAILY_TWILIO_CALLS: int = int(os.getenv("MAX_DAILY_TWILIO_CALLS", "5"))
    MAX_DAILY_TWILIO_MINUTES: int = int(os.getenv("MAX_DAILY_TWILIO_MINUTES", "10"))

# Global settings instance
settings = Settings()

def get_cost_protection():
    """Get cost protection instance"""
    from .cost_protection import CostProtection
    return CostProtection()
