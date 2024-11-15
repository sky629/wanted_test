from functools import wraps

from fastapi import Header, HTTPException

from app.config.settings import Settings

settings = Settings()


def validate_language_header(func):
    @wraps(func)
    async def wrapper(*args, x_wanted_language: str = Header(...), **kwargs):
        valid_languages = list(settings.LANGUAGE_CHOICES.keys())
        if x_wanted_language not in valid_languages:
            raise HTTPException(status_code=400, detail="잘못된 언어코드 입니다.")
        return await func(*args, x_wanted_language=x_wanted_language, **kwargs)

    return wrapper
