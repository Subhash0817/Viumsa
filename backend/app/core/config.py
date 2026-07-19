from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Viumsa"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "An Agentic AI Platform"

    class Config:
        env_file = ".env"


settings = Settings()