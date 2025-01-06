from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.util import await_only

from database.database import get_db, SessionLocal
from error import Missing
from resume import services
from resume.model import Resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.get("/all")
async def get_all_resumes(
        db: SessionLocal = Depends(get_db),
        limit: int = 0,
        skip: int = 0,
):
    try:
        return await services.get_all_resumes(db, limit, skip)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.get("/{title}")
async def get_resume_by_title(title: str) -> Resume:
    try:
        return await services.get_resume_by_title(title)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
