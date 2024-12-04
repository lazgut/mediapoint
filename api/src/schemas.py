from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class DataEntryCreate(BaseModel):
    content: str = Field(..., description="Content to be processed", example="Hello, Kafka!")


class DataEntry(DataEntryCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at', mode='plain', return_type='str', when_used='json')
    def serialize_datetime(value):
        return value.strftime('%Y-%m-%dT%H:%M:%S')


class Message(BaseModel):
    id: int
    message: str
