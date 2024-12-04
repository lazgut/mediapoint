from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DataEntryCreate(BaseModel):
    content: str = Field(..., description="Content to be processed", example="Hello, Kafka!")


class DataEntry(DataEntryCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    id: int
    message: str
