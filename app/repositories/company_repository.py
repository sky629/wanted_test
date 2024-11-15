from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import CompanyTag
from app.models.company import Company, CompanyName
from app.models.tag import Tag, TagName


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_by_name_partial(self, query: str, language: str = "ko") -> List[CompanyName]:
        """회사명 자동완성을 위한 부분 검색"""
        queryset = (
            select(CompanyName)
            .filter(CompanyName.language_code == language)
            .filter(CompanyName.name.ilike(f"%{query}%"))
            .order_by(CompanyName.name)
        )
        return self.db.execute(queryset).scalars().all()

    def get_by_name(self, name: str, language_code: str = None) -> Optional[Company]:
        """회사명으로 회사 검색"""
        queryset = (
            select(Company)
            .join(CompanyName)
            .filter(CompanyName.name == name)
            .options(
                joinedload(Company.company_names),
                joinedload(Company.company_tags)
                .joinedload(CompanyTag.tag)
                .joinedload(Tag.tag_names),
            )
        )
        if language_code:
            queryset = queryset.filter(CompanyName.language_code == language_code)

        return self.db.execute(queryset).unique().scalar_one_or_none()

    def create_company(self, company: Company) -> Company:
        """새로운 회사 생성"""
        self.db.add(company)
        self.db.flush()
        self.db.commit()
        return company

    def add_company_name(self, company_name: CompanyName) -> CompanyName:
        """회사명 추가"""
        self.db.add(company_name)
        self.db.flush()
        self.db.commit()
        return company_name

    def add_company_tag(self, company_tag: CompanyTag) -> CompanyTag:
        """회사에 태그 추가"""
        self.db.add(company_tag)
        self.db.flush()
        self.db.commit()
        return company_tag

    def remove_company_tag(self, company_id: int, tag_id: int) -> bool:
        """회사에서 태그 제거"""
        result = (
            self.db.query(CompanyTag)
            .filter(CompanyTag.company_id == company_id, CompanyTag.tag_id == tag_id)
            .delete()
        )
        return result > 0

    def get_companies_by_tag(self, tag_name: str, language: str) -> List[Company]:
        """태그명으로 회사 검색"""
        queryset = (
            select(Company)
            .join(CompanyTag)
            .join(Tag)
            .join(TagName)
            .filter(TagName.name == tag_name)
            .options(joinedload(Company.names), joinedload(Company.tags))
            .distinct()
        )
        return self.db.execute(queryset).unique().scalars().all()
