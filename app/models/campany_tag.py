from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class CompanyTag(BaseModel):
    __tablename__ = "company_tag"

    company_id = Column(BigInteger, ForeignKey("company.id"), primary_key=True)
    tag_id = Column(BigInteger, ForeignKey("tag.id"), primary_key=True)

    company = relationship("Company", back_populates="company_tags")
    tag = relationship("Tag", back_populates="company_tags")
