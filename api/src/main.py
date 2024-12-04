from contextlib import asynccontextmanager

from api.v1 import api_router
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from services.broker.producer import kafka_producer_instance


@asynccontextmanager
async def lifespan(app_fastapi: FastAPI):
    """Обработать старт приложения."""
    logger.info('API service started')
    await kafka_producer_instance.start()
    logger.info("Kafka producer initialized.")
    yield
    await kafka_producer_instance.stop()
    logger.info("Kafka producer stopped.")
    logger.info('API service stopped')


app = FastAPI(lifespan=lifespan, title=settings.service_name, docs_url='/api/v1',
              openapi_url='/api/v1/openapi.json', default_response_class=ORJSONResponse)

app.include_router(api_router, prefix='/api/v1')
