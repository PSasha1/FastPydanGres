import os

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

type DatabaseURL = str

class DatabaseSettings(BaseSettings):
    USER: str = 'postgres'
    PASSWORD: str = 'postgres'
    HOST: str = 'localhost'
    PORT: str = '5432'
    NAME: str = 'db'
    ECHO: bool = False

    @computed_field
    @property
    def url(self) -> DatabaseURL:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        extra='ignore'
    )

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "app"
    DEBUG: bool = True
    DOCS_OFFLINE: bool = True

    DB: DatabaseSettings = DatabaseSettings()

settings = Settings()