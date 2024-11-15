from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyNameSchema(BaseModel):
    id: int
    company_id: int
    language_code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagNameSchema(BaseModel):
    id: int
    tag_id: int
    language_code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagSchema(BaseModel):
    id: int
    tag_names: List[TagNameSchema]

    model_config = ConfigDict(from_attributes=True)


class CompanySchema(BaseModel):
    id: int
    company_names: Optional[List[CompanyNameSchema]] = []
    tage_names: Optional[List[TagNameSchema]] = []

    model_config = ConfigDict(from_attributes=True)


class CompanyTagSchema(BaseModel):
    company_id: int
    tag_id: int

    model_config = ConfigDict(from_attributes=True)


class CompanyNameRequest(BaseModel):
    ko: Optional[str] = Field(default=None)
    en: Optional[str] = Field(default=None)
    ja: Optional[str] = Field(default=None)
    tw: Optional[str] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class TagNameRequest(BaseModel):
    tag_name: Dict[str, str]

    model_config = ConfigDict(from_attributes=True)


class CompanyRequest(BaseModel):
    company_name: CompanyNameRequest
    tags: List[TagNameRequest]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "company_name": {"ko": "라인 프레쉬", "tw": "LINE FRESH", "en": "LINE FRESH"},
            "tags": [
                {"tag_name": {"ko": "태그_1", "tw": "tag_1", "en": "tag_1"}},
                {"tag_name": {"ko": "태그_8", "tw": "tag_8", "en": "tag_8"}},
                {"tag_name": {"ko": "태그_15", "tw": "tag_15", "en": "tag_15"}},
            ],
        },
    )


class CompanyResponse(BaseModel):
    company_name: str
    tags: List[str] = []

    model_config = ConfigDict(from_attributes=True)
