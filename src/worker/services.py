from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from error import Missing
from worker.model import Worker
from worker.schemas import WorkerCreateSchema


async def get_worker(name: str, db: AsyncSession) -> Worker:
    query = select(Worker).filter(Worker.name == name)
    result = await db.execute(query)
    if not result:
        raise Missing(msg=f"Worker with name = {name} is not found")
    return result.scalars().one()


async def get_all_workers(db: AsyncSession, limit: int, skip: int) -> list[Worker]:
    query = select(Worker).offset(skip).limit(limit)
    result = await db.execute(query)
    if not result:
        raise Missing(
            msg=f"There is no workers in database",
        )
    return [worker for worker in result.scalars().all()]


async def create_worker(data: WorkerCreateSchema, db: AsyncSession) -> Worker:
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


async def update_worker(data: WorkerCreateSchema, db: AsyncSession) -> Worker:
    stmt = (
        update(Worker)
        .filter(Worker.name == data.name)
        .values(
            name=data.name,
            email=data.email,
            hashed_password=data.hashed_password,
        )
    )
    db.add(stmt)
    await db.commit()
    worker = get_worker(data.name, db)
    return worker


async def delete_worker(name: str, db: AsyncSession):
    worker = await get_worker(name, db)
    if not worker:
        raise Missing(msg=f"Worker with name = {name} is not found")
    await db.delete(worker)
    await db.commit()
    return worker
