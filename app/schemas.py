from pydantic import BaseModel
from logger import logger
from datetime import date
from typing import List


# Pydantic model for data item
class DataEntryCreate(BaseModel):
    name: str
    id: int
    order_id: str
    order_creation_at: str

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"DataEntryCreate schema initialized with {data}")


class DataEntryResponse(BaseModel):
    id: int
    name: str
    order_id: str
    order_creation_at: date

    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()  # Custom serialization to string
        }
    
    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"DataEntryResponse schema initialized with {data}")


class PaginatedResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    items: List[DataEntryResponse]

    class Config:
        orm_mode = True  # This ensures SQLAlchemy models can be parsed correctly to Pydantic models