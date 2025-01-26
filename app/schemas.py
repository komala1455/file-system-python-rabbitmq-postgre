from pydantic import BaseModel
from logger import logger

# Pydantic model for data item
class DataEntryCreate(BaseModel):
    name: str
    id: int
    orderid: str
    date: str

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"DataEntryCreate schema initialized with {data}")

class DataEntryResponse(BaseModel):
    id: int
    name: str
    orderid: str
    date: str

    class Config:
        orm_mode = True
    
    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"DataEntryResponse schema initialized with {data}")