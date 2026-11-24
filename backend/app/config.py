from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    keitaro_api_url: str
    keitaro_api_key: str
    database_url: str = "sqlite:///./keitaro.db"

    class Config:
        env_file = ".env"

settings = Settings()