from api.v1.endpoints import data_entry
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(data_entry.router, prefix='/data', tags=['Данные'])
