from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException

from app.common.decorators import validate_language_header
from app.common.dependencies import get_company_service
from app.schemas.company import CompanyRequest, TagNameRequest
from app.services.company_service import CompanyService

router = APIRouter()


@router.get("/search")
@validate_language_header
async def search_company(
    query: str,
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    """
    회사명 자동완성 검색
    - **query**: 회사명의 일부만 들어가도 검색
    - **x_wanted_language**:  header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    # key = query+x_wanted_language
    # key = key.replace(" ", "")
    # companies = service.cache_repository.get_data_by_key()
    # if companies is None:
    #     companies = service.search_companies_by_name(query, x_wanted_language)
    #     service.cache_repository.set_data_by_key(key, companies, 10)

    companies = service.search_companies_by_name(query, x_wanted_language)

    return companies


@router.get("/companies/{company_name}")
@validate_language_header
async def get_company(
    company_name: str,
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    """
    회사 이름으로 회사 검색
    - **company_name**: 정확한 회사 이름
    - **x_wanted_language**: header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    company = service.get_company_by_name(company_name, x_wanted_language)
    if not company:
        raise HTTPException(status_code=404)
    return company


@router.post("/companies")
@validate_language_header
async def create_company(
    company: CompanyRequest,
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    """
    새로운 회사 추가
    - **company**: 회사 정보 데이터
    - **x_wanted_language**: 저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    return service.create_company(company, x_wanted_language)


@router.get("/tags")
@validate_language_header
async def search_by_tag(
    query: str,
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    """
    태그명으로 회사 검색
     - **query**: 정확한 태그 네임이어야 합니다.
     - **x_wanted_language**: header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    return service.search_companies_by_tag(query, x_wanted_language)


@router.put("/companies/{company_name}/tags")
async def add_company_tags(
    company_name: str,
    tags: List[TagNameRequest],
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    """
    회사 태그 정보 추가
    - **company_name**: 정확한 회사 이름
     - **tags**: 태그 리스트
     - **x_wanted_language**: 저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    return service._add_company_to_tags(company_name, tags, x_wanted_language)


@router.delete("/companies/{company_name}/tags/{tag_name}")
@validate_language_header
async def delete_company_tag(
    company_name: str,
    tag_name: str,
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    """
    회사 태그 정보 삭제
    - **company_name**: 정확한 회사 이름
     - **tag_name**: 정확한 태그 이름
     - **x_wanted_language**: 삭제 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    return service.delete_company_tag(company_name, tag_name, x_wanted_language)
