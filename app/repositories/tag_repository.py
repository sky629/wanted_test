from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import CompanyTag
from app.models.company import Company
from app.models.tag import Tag, TagName


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str, language: str = None) -> Optional[Tag]:
        print(f"-------------- {name} / {language}")
        """태그명으로 태그 검색"""
        queryset = select(Tag).join(TagName)
        if language:
            queryset = queryset.filter(TagName.language_code == language, TagName.name == name)
        else:
            queryset = queryset.filter(TagName.name == name)
        return self.db.execute(queryset).scalar_one_or_none()

    def get_companies_by_tag_name(self, tag_query: str) -> List[Company]:
        """
        태그명으로 회사 검색
        """
        queryset = (
            select(Company)
            .distinct()
            .join(CompanyTag)
            .join(Tag)
            .join(TagName)
            .filter(TagName.name == tag_query)
            .options(
                joinedload(Company.company_names),
                joinedload(Company.company_tags)
                .joinedload(CompanyTag.tag)
                .joinedload(Tag.tag_names),
            )
            .order_by(Company.id)
        )

        return self.db.execute(queryset).unique().scalars().all()

    def create_tag(self, tag: Tag) -> Tag:
        """새로운 태그 생성"""
        self.db.add(tag)
        self.db.flush()
        self.db.commit()
        return tag

    def add_tag_name(self, tag_name: TagName) -> TagName:
        """태그명 추가"""
        self.db.add(tag_name)
        self.db.flush()
        self.db.commit()
        return tag_name

    def get_or_create_tag(self, name: str, language_code: str) -> Tag:
        """태그명으로 태그 검색 또는 생성"""
        try:
            # 기존 태그 검색
            tag = self.get_by_name(name, language_code)
            if tag:
                return tag

            # 새 태그 생성
            tag = Tag()
            self.db.add(tag)
            self.db.flush()

            # 태그명 추가
            tag_name = TagName(tag_id=tag.id, language_code=language_code, name=name)
            self.db.add(tag_name)
            self.db.flush()

            return tag

        except Exception:
            self.db.rollback()
            raise

    def get_tag_names(self, tag_id: int, language: str = None) -> List[TagName]:
        """태그의 다국어 이름 조회"""
        queryset = select(TagName).filter(TagName.tag_id == tag_id)
        if language:
            queryset = queryset.filter(TagName.language_code == language)
        return self.db.execute(queryset).scalars().all()
