from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    UPLOAD_DIR: str = '/tmp/sketch3d'
    MAX_UPLOAD_MB: int = 20
    CORS_ORIGINS: list[str] = ['http://localhost:5173']
    TESSERACT_CMD: str = '/usr/bin/tesseract'
    LOG_LEVEL: str = 'INFO'


@lru_cache
def get_settings() -> Settings:
    return Settings()
