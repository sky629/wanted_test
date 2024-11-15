from fastapi import FastAPI

from app.config.settings import Settings
from app.routers import company, index

settings = Settings()

# FastAPI 앱 생성
app = FastAPI()


app.include_router(index.router, prefix="/api")
app.include_router(company.router, prefix="")
