from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db

router = APIRouter(
    prefix="/worker",
    tags=["Worker"],
)


@router.get("/{name}")
async def get_worker(name: str, db: Session = Depends(get_db)):
    worker = service.get_worker(name, db)
    if not worker:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with name = {name} is not found",
        )
    return worker
