from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from error import Missing, Duplicate
from resume.model import Resume
from resume.schemas import GetResumesByNameSchema, CreateResumeSchema, UpdateResumeSchema


async def get_resume_by_id(id: int, db: AsyncSession) -> Resume:
    query = select(Resume).filter_by(id=id)
    result = await db.execute(query)
    return result.scalars().one()


async def get_resume_by_title(title: GetResumesByNameSchema, db: AsyncSession) -> Resume:
    query = select(Resume).filter_by(title=title)
    result = await db.execute(query)
    return result.scalars().one()


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
        limit: int = 1,
        skip: int = 0,
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
    return await get_resume_by_id(new_resume.id, db)


async def update_resume(
        title: UpdateResumeSchema,
        data: CreateResumeSchema,
        db: AsyncSession,
) -> Resume:
    resume = await get_resumes_by_title(title, db)[0]
    for key, value in data.items():
        if value is not None:
            resume.key = value
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return await get_resume_by_id(resume.id, db)


async def delete_resume(
        title: GetResumesByNameSchema,
        db: AsyncSession,
) -> Resume:
    resume_to_delete = await get_resumes_by_title(title, db)[0]
    if resume_to_delete:
        await db.delete(resume_to_delete)
        return resume_to_delete
    raise Missing(
        msg=f"There is no resume with title = {title} in database",
    )
