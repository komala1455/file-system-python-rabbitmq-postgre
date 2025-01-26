from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_connection
from models import DataEntry
from schemas import DataEntryResponse, PaginatedResponse
from sqlalchemy import func
from typing import List

router = APIRouter()

# Pagination helper function
def paginate_query(query, page: int = 1, page_size: int = 10):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be >= 1")
    if page_size < 1:
        raise HTTPException(status_code=400, detail="Page size must be >= 1")
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)

@router.get("/data", response_model=PaginatedResponse)
def read_data(name: str = None, order_id: str = None, page: int = 1, size: int = 10, db: Session = Depends(get_connection)):
    # Start building the query
    total_items = None
    query = db.query(DataEntry)
    if name:
        query = query.filter(DataEntry.name.ilike(f"%{name}%"))
        total_items = query.count()
    if order_id:
        query = query.filter(DataEntry.order_id == order_id)

    # Apply pagination
    objs = paginate_query(query, page=page, page_size=size)
    # Fetch results
    results = objs.all()
    if not results:
        error_msg = "No data entries found"
        if name:
            error_msg += f" for name {name}"
        if order_id:
            error_msg += f" with order ID {order_id}"
        raise HTTPException(status_code=404, detail=error_msg)
    # Calculate total items and pages
    if total_items is None:
        total_items = db.query(func.count(DataEntry.id)).scalar()
    total_pages = (total_items + size - 1) // size  # ceil division
    # Prepare the response data
    return PaginatedResponse(
        page=page,
        page_size=size,
        total_items=total_items,
        total_pages=total_pages,
        items=[DataEntryResponse.from_orm(item) for item in results]
    )