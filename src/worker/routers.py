from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import services
from database.database import get_db
from worker.schemas import WorkerGetSchema, WorkerCreateSchema

router = APIRouter(
    prefix="/worker",
    tags=["Worker"],
)


@router.get("/{name}")
async def get_worker(
        name: WorkerGetSchema,
        db: AsyncSession = Depends(get_db),
    ):
    return services.get_worker(name, db)


@router.get("/all")
async def get_all_workers(
        db: AsyncSession = Depends(get_db),
        limit: int = 0,
        skip: int = 0,
    ):
    return services.get_all_workers(db, limit, skip)


@router.post("/create")
async def create_worker(
        data: WorkerCreateSchema,
        db: AsyncSession = Depends(get_db),
    ):
    return services.create_worker(data, db)
