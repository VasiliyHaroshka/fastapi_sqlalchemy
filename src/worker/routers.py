from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from worker import services
from worker.model import Worker

router = APIRouter(
    prefix="/worker",
    tags=["Worker"],
)


@router.get("/{name}")
async def get_worker(name: str, db: Session = Depends(get_db)):
    return services.get_worker(name, db)
