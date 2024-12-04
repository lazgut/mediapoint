from typing import Generic, Type, TypeVar

from fastapi import HTTPException
from loguru import logger
from models import Base
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType]):
    """Базовый CRUD сервис для моделей SQLAlchemy."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get(self, _id: int) -> ModelType:
        logger.info(f"Fetching {self.model.__name__} with ID: {_id}")
        query = select(self.model).where(self.model.id == _id)
        obj = await self.db_session.scalar(query)
        if obj is None:
            logger.warning(f"{self.model.__name__} with ID {_id} not found.")
            raise HTTPException(status_code=404, detail='Not found')
        logger.info(f"Found {self.model.__name__} with ID: {_id}")
        return obj

    async def get_list(self) -> list[ModelType]:
        logger.info(f"Fetching list of {self.model.__name__}")
        query = select(self.model)
        objs = await self.db_session.scalars(query)
        objs = [obj for obj in objs.all()]
        logger.info(f"Retrieved {len(objs)} {self.model.__name__}(s).")
        return objs

    async def create(self, obj: CreateSchemaType) -> int:
        logger.info(f"Creating new {self.model.__name__}")
        db_obj = self.model(**obj.model_dump())
        self.db_session.add(db_obj)
        await self.db_session.flush()
        logger.info(f"Created {self.model.__name__} with ID: {db_obj.id}")
        return db_obj.id
