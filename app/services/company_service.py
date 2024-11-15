from typing import Dict, List

from fastapi import HTTPException

from app.models import CompanyTag
from app.models.company import Company, CompanyName
from app.models.tag import TagName
from app.repositories.company_repository import CompanyRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.company import CompanyRequest, CompanyResponse, TagNameRequest


class CompanyService:
    def __init__(self, company_repository: CompanyRepository, tag_repository: TagRepository):
        self.company_repository = company_repository
        self.tag_repository = tag_repository

    def search_companies_by_name(self, query: str, language: str) -> List[dict]:
        """회사명 자동 완성 조회"""
        companies = self.company_repository.search_by_name_partial(query, language)
        return [{"company_name": c.name} for c in companies]

    def get_company_by_name(self, name: str, language: str) -> CompanyResponse:
        """회사 상세 정보 조회"""
        company = self.company_repository.get_by_name(name)
        if not company:
            raise HTTPException(status_code=404, detail="회사를 찾을수 없습니다.")
        return self._format_company_response(company, language)

    def create_company(self, request: CompanyRequest, language: str) -> CompanyResponse:
        """새로운 회사 생성"""
        company = Company()
        self.company_repository.create_company(company)

        # 회사명 추가
        for lang, name in request.company_name.dict(exclude_unset=True).items():
            # 중복 확인
            existing_company_name = self.company_repository.get_by_name(name, lang)
            if not existing_company_name:
                company_name = CompanyName(company=company, language_code=lang, name=name)
                self.company_repository.add_company_name(company_name)
            else:
                raise HTTPException(status_code=400, detail="회사가 이미 존재합니다.")

        # 태그 추가
        for tag_request in request.tags:
            self._add_tag_to_company(company, tag_request.tag_name)

        # 다 되면 적용
        self.company_repository.db.commit()
        return self._format_company_response(company, language)

    def _add_tag_to_company(self, company: Company, tag_names: Dict[str, str]) -> None:
        """회사에 태그 추가"""
        # 첫 번째 언어의 태그명으로 태그 검색 또는 생성
        first_lang = next(iter(tag_names))
        tag = self.tag_repository.get_or_create_tag(tag_names[first_lang], first_lang)

        # 나머지 언어의 태그명 추가
        for lang, name in tag_names.items():
            if lang != first_lang:
                # 중복 확인 후 태그명 추가
                existing_tag_name = self.tag_repository.get_by_name(name, lang)
                if not existing_tag_name:
                    tag_name = TagName(tag=tag, language_code=lang, name=name)
                    self.tag_repository.add_tag_name(tag_name)

        # 회사와 태그 연결
        company_tag = CompanyTag(company_id=company.id, tag_id=tag.id)
        self.company_repository.add_company_tag(company_tag)

    def _format_company_response(self, company: Company, language: str) -> CompanyResponse:
        """회사 정보를 응답 형식으로 변환"""
        # 요청된 언어의 회사명 찾기
        name = None
        for n in company.company_names:
            if n.language_code == language:
                name = n.name
                break
        # 없으면 첫 번째 이름 사용
        if name is None and company.company_names:
            name = company.company_names[0].name

        # 회사명이 여전히 None인 경우 예외 처리
        if name is None:
            raise HTTPException(status_code=404, detail="회사를 찾을수 없습니다.")

        # 요청된 언어의 태그명 수집
        tags = []
        for company_tag in company.company_tags:
            tag_name = None
            for tn in company_tag.tag.tag_names:
                if tn.language_code == language:
                    tag_name = tn.name
                    break
            # 없으면 첫 번째 이름 사용
            if tag_name is None and company_tag.tag.tag_names:
                tag_name = company_tag.tag.tag_names[0].name
            if tag_name:
                tags.append(tag_name)

        return CompanyResponse(company_name=name, tags=sorted(tags))

    def search_companies_by_tag(self, tag_query: str, language: str) -> List[CompanyResponse]:
        """
        태그명으로 회사 검색
        """
        companies = self.tag_repository.get_companies_by_tag_name(tag_query)

        # 중복 제거 및 응답 형식으로 변환
        return [self._format_company_response(company, language) for company in companies]

    def _add_company_to_tags(
        self, company_name: str, tag_requests: List[TagNameRequest], language: str
    ) -> CompanyResponse:
        """회사에 태그 추가"""
        # 회사 조회
        company = self.company_repository.get_by_name(company_name)
        if not company:
            raise HTTPException(status_code=404, detail="회사를 찾을수 없습니다.")

        # 태그 추가
        for tag_request in tag_requests:
            # 중복 확인
            for lang, name in tag_request.tag_name.items():
                existing_tag = self.tag_repository.get_by_name(name, lang)
                if existing_tag:
                    raise HTTPException(status_code=400, detail="태그가 이미 존재합니다.")
            self._add_tag_to_company(company, tag_request.tag_name)

        # 다 되면 적용
        self.company_repository.db.commit()
        return self._format_company_response(company, language)

    def delete_company_tag(
        self, company_name: str, tag_name: str, language: str
    ) -> CompanyResponse:
        """회사의 태그 삭제"""
        # 회사 조회
        company = self.company_repository.get_by_name(company_name)
        if not company:
            raise HTTPException(status_code=404, detail="회사를 찾을수 없습니다.")

        # 태그 조회
        tag_to_delete = None
        for company_tag in company.company_tags:
            for tag in company_tag.tag.tag_names:
                if tag.name == tag_name and tag.language_code == language:
                    tag_to_delete = company_tag.tag
                    company.company_tags.remove(company_tag)
                    break
            if tag_to_delete:
                break

        if not tag_to_delete:
            raise HTTPException(status_code=404, detail="회사에 연결된 태그를 찾을수 없습니다.")

        if len(company.company_tags) == 0:
            raise HTTPException(status_code=400, detail="회사에 최소 하나의 태그가 연결돼 있어야 합니다.")

        # 회사와 태그 연결 삭제
        success = self.company_repository.remove_company_tag(company.id, tag_to_delete.id)
        if not success:
            raise HTTPException(status_code=404, detail="태그 삭제 실패")

        # 다 되면 적용
        self.company_repository.db.commit()

        return self._format_company_response(company, language)
