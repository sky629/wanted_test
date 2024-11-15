import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings

settings = Settings()

engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, autocommit=False)

RedisClient = redis.StrictRedis(
    host=settings.redis_host, port=settings.redis_port, db=settings.redis_db, decode_responses=True
)
