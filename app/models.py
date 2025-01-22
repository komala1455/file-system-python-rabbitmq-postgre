from sqlalchemy import Column, Integer, String, Date
from database import Base
from config import TABLE_NAME
from logger import logger

class DataEntry(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable = False)
    orderid = Column(String, nullable = False)
    date = Column(Date, nullable = False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"DataEntry created with {kwargs}")
