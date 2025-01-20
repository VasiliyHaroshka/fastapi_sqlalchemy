from fastapi import APIRouter, Depends, HTTPException

from database.database import get_db, SessionLocal
from error import Missing, Duplicate
from resume import services
from resume.model import Resume
from resume.schemas import GetResumesByNameSchema, CreateResumeSchema, UpdateResumeSchema

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
        title: str,
        db: SessionLocal = Depends(get_db),
        limit: int = 0,
        skip: int = 0,
):
    try:
        return await services.get_resumes_by_title(title, db, limit, skip)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("/create")
async def create_resume(
        data: CreateResumeSchema,
        db: SessionLocal = Depends(get_db),
):
    try:
        await services.create_resume(data, db)
    except Duplicate as e:
        return HTTPException(status_code=409, detail=e.msg)


@router.patch("/{title}")
async def update_resume(
        title: str,
        data: UpdateResumeSchema,
        db: SessionLocal = Depends(get_db),
):
    try:
        return await services.update_resume(title, data, db)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.delete("/{title}")
async def delete_resume(
        title: str,
        db: SessionLocal = Depends(get_db),
):
    try:
        return await services.delete_resume(title, db)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
