from fastapi import FastAPI

from worker.routers import router as worker_router
from resume.routers import router as resume_router

app = FastAPI()

app.include_router(worker_router)
app.include_router(resume_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
