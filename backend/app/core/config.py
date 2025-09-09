from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenAI Hackathon"
    API_V1_PREFIX: str = "/v1"
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()

OLLAMA_MODEL = 'gpt-oss:20b'