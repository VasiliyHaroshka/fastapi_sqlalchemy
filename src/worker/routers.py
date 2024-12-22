from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from worker.model import Worker
from worker import services
from worker.schemas import WorkerGetSchema

router = APIRouter(
    prefix="/worker",
    tags=["Worker"],
)


@router.get("/{name}")
async def get_worker(name: WorkerGetSchema, db: Session = Depends(get_db)) -> Worker:
    return services.get_worker(name, db)


@router.get("/all")
async def get_all_workers(db: Session = Depends(get_db), limit: int, skip: int) -> list[Worker]:
    return services.get_all_workers(db, limit, skip)
