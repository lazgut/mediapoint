import uuid
from logging import getLogger

from core.config import settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

logger = getLogger(__name__)

engine = create_async_engine(
    url=settings.database_url, pool_size=settings.pool_size,
    max_overflow=settings.max_overflow, echo=False,
)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession,
    expire_on_commit=False, autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        try:
            await session.commit()
        except SQLAlchemyError as error:
            logger.exception(f'########   SQLALCHEMY ERROR SESSION  ---  {str(error)}   ##########')
            await session.rollback()
        finally:
            await session.close()
