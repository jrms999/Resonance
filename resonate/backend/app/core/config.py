from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "Resonate"
    API_V1_STR: str = "/api/v1"

    POSTGRES_DSN: AnyUrl
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
