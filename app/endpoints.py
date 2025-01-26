from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import DataEntry
from schemas import DataEntryResponse

router = APIRouter()

@router.get("/data", response_model=list[DataEntryResponse])
def read_data(name: str = None, page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    query = db.query(DataEntry)
    if name:
        query = query.filter(DataEntry.name == name)
    return query.offset((page - 1) * size).limit(size).all()
