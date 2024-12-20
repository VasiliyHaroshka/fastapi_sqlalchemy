from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from worker.model import Worker


async def get_worker(name: str, db: Session):
    query = select(Worker).filter(Worker.name == name)
    worker = await db.execute(query).scalars().one()
    if not worker:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with name = {name} is not found"
        )
    return worker
