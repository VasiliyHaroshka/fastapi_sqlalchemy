from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from worker.model import Worker


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
