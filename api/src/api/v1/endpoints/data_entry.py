from typing import Annotated

from core.config import settings
from fastapi import APIRouter, Body, Depends
from schemas import DataEntry, DataEntryCreate, Message
from services.broker.producer import KafkaProducerService, get_kafka_producer_service
from services.db.data_entry import DataEntryService, get_data_entry_service

router = APIRouter()


@router.post('', response_model=Message, status_code=201)
async def create(
    data_entry: Annotated[DataEntryCreate, Body()],
    db_service: Annotated[DataEntryService, Depends(get_data_entry_service)],
    kafka_producer_service: Annotated[KafkaProducerService, Depends(get_kafka_producer_service)]
):
    result = await db_service.create(data_entry)
    await kafka_producer_service.send_message(
        topic=settings.kafka_topic,
        key=b"data_entry",
        value=data_entry.content.encode()
    )
    return Message(id=result, message='Data saved and published to Kafka.')


@router.get('', response_model=list[DataEntry], status_code=200)
async def get_list(
    db_service: Annotated[DataEntryService, Depends(get_data_entry_service)],
):
    result = await db_service.get_list()
    return result
