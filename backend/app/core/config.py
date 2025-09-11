from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenAI Hackathon"
    API_V1_PREFIX: str = "/v1"
    OPENAI_API_KEY: str
    GOOGLE_MAPS_API_KEY: str
    TWILIO_PHONE_NUMBER: str
    ACCOUNT_SID: str
    AUTH_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()

OLLAMA_MODEL = 'gpt-oss:20b'