"""Модуль настроек сервиса API."""
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Настройки API сервиса."""

    # Service
    service_name: str = Field(..., validation_alias='SERVICE_NAME')
    # Uvicorn
    uvicorn_app_name: str = Field(..., validation_alias='UVICORN_APP_NAME')
    uvicorn_host: str = Field(..., validation_alias='UVICORN_HOST')
    uvicorn_port: int = Field(..., validation_alias='UVICORN_PORT')
    uvicorn_workers: int = Field(..., validation_alias='UVICORN_WORKERS')
    uvicorn_timeout: int = Field(..., validation_alias='UVICORN_TIMEOUT')
    # PostgreSQL
    database_url: str = Field(..., validation_alias='DATABASE_URL')
    postgres_timeout: int = Field(..., validation_alias='POSTGRES_TIMEOUT')
    pool_size: int = Field(..., validation_alias='POOL_SIZE')
    max_overflow: int = Field(..., validation_alias='MAX_OVERFLOW')
    sql_batch_size: int = Field(..., validation_alias='SQL_BATCH_SIZE')
    # Kafka
    kafka_broker: str = Field(..., validation_alias='KAFKA_BROKER')
    kafka_topic: str = Field(..., validation_alias='KAFKA_TOPIC')
    # Logger
    logger_name: str = Field(..., validation_alias='LOGGER_NAME')
    logger_level: int = Field(..., validation_alias='APP_DEBUG_LEVEL')

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, 'core', '.env'))


settings = Settings()
