from fastapi import APIRouter

router = APIRouter(
    prefix="/worker",
    tags=["Worker"],
)
