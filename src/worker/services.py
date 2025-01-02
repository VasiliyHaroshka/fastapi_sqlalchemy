from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from worker.model import Worker
from worker.schemas import WorkerCreateSchema


async def get_worker(name: str, db: AsyncSession) -> Worker:
    query = select(Worker).filter(Worker.name == name)
    worker = await db.execute(query).scalars().one()
    if not worker:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with name = {name} is not found",
        )
    return worker


async def get_all_workers(db: AsyncSession, limit: int, skip: int) -> list[Worker]:
    query = select(Worker).offset(skip).limit(limit)
    workers = await db.execute(query).scalars().all()
    if not workers:
        raise HTTPException(
            status_code=404,
            detail=f"There is no workers in database",
        )
    return workers


async def create_worker(data, db: AsyncSession) -> Worker:
    new_worker = Worker(
        name=data["name"],
        hashed_password=data["hashed_password"],
        email=data["email"],
    )
    if not new_worker:
        raise HTTPException(
            status_code=409,
            detail=f"Can't create new worker, try again",
        )
    db.add(new_worker)
    await db.commit()
    await db.refresh(new_worker)
    return new_worker


async def update_worker(data: WorkerCreateSchema, db: AsyncSession) -> Worker | dict:
    worker = get_worker(data.name, db)
    if not worker:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with name = {data.name} is not found",
        )
    worker.name = data.name
    worker.email = data.email
    worker.hashed_password = data.hashed_password
    db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker



async def delete_worker(name: str, db: AsyncSession):
    worker = await get_worker(name, db)
    if not worker:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with name = {name} is not found",
        )
    await db.delete(worker)
    await db.commit()
    return worker
