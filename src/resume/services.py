from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from error import Missing
from resume.model import Resume


async def get_all_resumes(db: AsyncSession, limit: int, skip: int) -> list[Resume]:
    query = select(Resume).offset(skip).limit(limit)
    result = await db.execute(query)
    if not result:
        raise Missing(
            msg=f"There is no resume in database",
        )
    return [resume for resume in result.scalars().all()]


async def get_resumes_by_title(
        title: str,
        db: AsyncSession,
        limit,
        skip,
) -> list[Resume]:

    query = select(Resume).filter_by(title=title).offset(skip).limit(limit)
    result = await db.execute(query)
    if not result:
        raise Missing(
            msg=f"There is no resume with title = {title} in database",
        )
    return [resume for resume in result.scalars().all()]
