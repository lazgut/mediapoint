from typing import Generic, Type, TypeVar

from fastapi import HTTPException
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
        query = select(self.model).where(self.model.id == _id)
        obj = await self.db_session.scalar(query)
        if obj is None:
            raise HTTPException(status_code=404, detail='Не найдено')
        return obj

    async def get_list(self) -> list[ModelType]:
        query = select(self.model)
        objs = await self.db_session.scalars(query)
        objs = [obj for obj in objs.all()]
        return objs

    async def create(self, obj: CreateSchemaType) -> int:
        db_obj = self.model(**obj.model_dump())
        self.db_session.add(db_obj)
        await self.db_session.flush()
        return db_obj.id
