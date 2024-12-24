from fastapi import APIRouter, Depends
from sqlalchemy.orm.sync import update

import services
from database.database import get_db, SessionLocal
from worker.schemas import WorkerGetSchema, WorkerCreateSchema

router = APIRouter(
    prefix="/worker",
    tags=["Worker"],
)


@router.get("/{name}")
async def get_worker(
        name: WorkerGetSchema,
        db: SessionLocal = Depends(get_db),
):
    return services.get_worker(name, db)


@router.get("/all")
async def get_all_workers(
        db: SessionLocal = Depends(get_db),
        limit: int = 0,
        skip: int = 0,
):
    return services.get_all_workers(db, limit, skip)


@router.post("/create")
async def create_worker(
        data: WorkerCreateSchema,
        db: SessionLocal = Depends(get_db),
):
    return services.create_worker(data, db)
