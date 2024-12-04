from services.db.postgres import get_session
from fastapi import Depends
from models import DataEntry
from schemas import DataEntryCreate
from services.db.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class DataEntryService(BaseService[DataEntry, DataEntryCreate]):

    def __init__(self, db_session: AsyncSession):
        super(DataEntryService, self).__init__(DataEntry, db_session)


async def get_data_entry_service(
    db_session: AsyncSession = Depends(get_session)
) -> DataEntryService:
    return DataEntryService(db_session)
