from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.company_repository import CompanyRepository
from app.repositories.tag_repository import TagRepository
from app.services.company_service import CompanyService

from .database import RedisClient, SessionLocal


def get_db():
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()


def get_redis() -> RedisClient:
    with RedisClient() as redis_client:
        try:
            yield redis_client
        finally:
            redis_client.close()


def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepository:
    return CompanyRepository(db)


def get_tag_repository(db: Session = Depends(get_db)) -> TagRepository:
    return TagRepository(db)


def get_company_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    tag_repository: TagRepository = Depends(get_tag_repository),
) -> CompanyService:
    return CompanyService(company_repository=company_repository, tag_repository=tag_repository)
