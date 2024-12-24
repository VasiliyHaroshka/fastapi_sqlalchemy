from zoneinfo import reset_tzpath

from fastapi import APIRouter, Depends, HTTPException

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


@router.patch("/update")
async def update_worker(
        data: WorkerCreateSchema,
        db: SessionLocal = Depends(get_db),
    ):
    worker = services.get_worker(name=data.name, db=db)
    if not worker:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with name = {data.name} is not found",
        )
    return services.update_worker(data, db)
