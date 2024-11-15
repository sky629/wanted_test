from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from app.config.settings import Settings
from app.models.base import BaseModel

settings = Settings()


class Tag(BaseModel):
    __tablename__ = "tag"

    tag_names = relationship("TagName", back_populates="tag")
    company_tags = relationship("CompanyTag", back_populates="tag")


class TagName(BaseModel):
    __tablename__ = "tag_name"

    tag_id = Column(BigInteger, ForeignKey("tag.id"), nullable=False)
    language_code = Column(
        Enum(*settings.LANGUAGE_CHOICES.keys(), name="language_code_enum"), nullable=False
    )
    name = Column(String(settings.MAX_TEXT_FIELD), nullable=False)

    tag = relationship("Tag", back_populates="tag_names")

    __table_args__ = (
        UniqueConstraint("tag_id", "language_code", "name", name="unique_tag_lang_name"),
    )
