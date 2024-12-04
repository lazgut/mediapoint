from contextlib import asynccontextmanager

from api.v1 import api_router
from core.config import settings
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from services.broker.producer import kafka_producer_instance
from starlette.exceptions import HTTPException as StarletteHTTPException


@asynccontextmanager
async def lifespan(app_fastapi: FastAPI):
    """Обработать старт приложения."""
    logger.info('API service started')
    await kafka_producer_instance.start()
    yield
    await kafka_producer_instance.stop()
    logger.info('API service stopped')


app = FastAPI(lifespan=lifespan, title=settings.service_name, docs_url='/api/v1',
              openapi_url='/api/v1/openapi.json', default_response_class=ORJSONResponse)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return ORJSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()},
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


app.include_router(api_router, prefix='/api/v1')
