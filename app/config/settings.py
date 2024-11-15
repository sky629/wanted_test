from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = Field(default="db", env="POSTGRES_HOST")
    postgres_port: str = Field(default="5432", env="POSTGRES_PORT")
    postgres_user: str = Field(default="postgres", env="POSTGRES_USER")
    postgres_password: str = Field(default="1234", env="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="wanted", env="POSTGRES_DB")
    redis_host: str = Field(default="redis", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")

    MAX_TEXT_FIELD: int = 255

    LANGUAGE_CHOICES: dict = {"ko": "한국어", "en": "영어", "jp": "일본어", "tw": "대만어"}

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
