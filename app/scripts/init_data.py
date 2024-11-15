import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings
from app.models.campany_tag import CompanyTag
from app.models.company import Company, CompanyName
from app.models.tag import Tag, TagName

settings = Settings()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_or_create_tag(session, tag_names: Dict[str, str], tag_cache: Dict[str, Tag]) -> Tag:
    ko_name = tag_names["ko"]

    if ko_name in tag_cache:
        return tag_cache[ko_name]

    tag = Tag()
    session.add(tag)
    session.flush()

    tag_names_list = []
    for lang, name in tag_names.items():
        if name:
            tag_name = TagName(tag_id=tag.id, language_code=lang, name=name)
            tag_names_list.append(tag_name)

    session.add_all(tag_names_list)
    tag_cache[ko_name] = tag
    return tag


def create_company_with_names(session, names: Dict[str, str]) -> Company:
    company = Company()
    session.add(company)
    session.flush()

    company_names = []
    for lang, name in names.items():
        if name:
            company_name = CompanyName(company_id=company.id, language_code=lang, name=name)
            company_names.append(company_name)

    session.add_all(company_names)
    return company


def import_data():
    session = SessionLocal()
    if session.query(Company).first() is not None:
        print("already init data.")
        return

    try:
        # CSV 파일 읽기
        csv_path = os.path.join(os.path.dirname(__file__), "company_tag_sample.csv")
        df = pd.read_csv(csv_path)
        df = df.where(pd.notnull(df), None)

        tag_cache: Dict[str, Tag] = {}

        for _, row in df.iterrows():
            # 회사 이름 처리
            company_names = {
                "ko": row["company_ko"],
                "en": row["company_en"],
                "jp": row["company_ja"],
            }
            company = create_company_with_names(session, company_names)

            # 태그 처리
            ko_tags = str(row["tag_ko"]).split("|")
            en_tags = str(row["tag_en"]).split("|")
            jp_tags = str(row["tag_ja"]).split("|")

            for ko, en, jp in zip(ko_tags, en_tags, jp_tags):
                tag_names = {"ko": ko.strip(), "en": en.strip(), "jp": jp.strip()}

                tag = get_or_create_tag(session, tag_names, tag_cache)

                company_tag = CompanyTag(company_id=company.id, tag_id=tag.id)
                session.add(company_tag)

            session.flush()

        session.commit()
        print("init data setting complete.")

    except Exception as e:
        session.rollback()
        print(f"error : {str(e)}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    import_data()
