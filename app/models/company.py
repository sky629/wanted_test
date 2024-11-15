from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from app.config.settings import Settings
from app.models.base import BaseModel

settings = Settings()


class Company(BaseModel):
    __tablename__ = "company"

    company_names = relationship("CompanyName", back_populates="company")
    company_tags = relationship("CompanyTag", back_populates="company")


class CompanyName(BaseModel):
    __tablename__ = "company_name"

    company_id = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    language_code = Column(
        Enum(*settings.LANGUAGE_CHOICES.keys(), name="language_code_enum"), nullable=False
    )
    name = Column(String(settings.MAX_TEXT_FIELD), nullable=False)

    company = relationship("Company", back_populates="company_names")

    __table_args__ = (UniqueConstraint("company_id", "language_code", name="unique_company_lang"),)
