from fastapi import APIRouter, Depends, HTTPException

from database.database import get_db, SessionLocal
from error import Missing
from resume import services
from resume.model import Resume
from resume.schemas import GetResumesByName

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
async def get_resumes_by_title(
        title: GetResumesByName,
        db: SessionLocal = Depends(get_db),
        limit: int = 0,
        skip: int = 0,
):
    try:
        return await services.get_resumes_by_title(title, db, limit, skip)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
