from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from error import Missing, Duplicate
from resume.model import Resume
from resume.schemas import GetResumesByNameSchema, CreateResumeSchema


async def get_all_resumes(db: AsyncSession, limit: int, skip: int) -> list[Resume]:
    query = select(Resume).offset(skip).limit(limit)
    result = await db.execute(query)
    if not result:
        raise Missing(
            msg=f"There is no resume in database",
        )
    return [resume for resume in result.scalars().all()]


async def get_resumes_by_title(
        title: GetResumesByNameSchema,
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


async def create_resume(data: CreateResumeSchema, db: AsyncSession) -> Resume:
    new_resume = Resume(
        title=data.title,
        description=data.description,
        salary=data.salary,
        workload=data.workload,
    )
    all_resumes = select(Resume)
    if new_resume in all_resumes:
        raise Duplicate(msg="This resume already exists in database")
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)
    query = select(Resume).filter_by(id=new_resume.id)
    result = await db.execute(query)
    return result.scalars().one()
