from typing import Any

from app.common.database import RedisClient


class CacheRepository:
    def __init__(self):
        self._redis_client = RedisClient

    def clean(self) -> None:
        self._redis_client.flushall()

    def get_data_by_key(self, key: str) -> Any:
        return self._redis_client.get(key)

    def set_data_by_key(self, key: str, data: Any, timeout: int = 10) -> None:
        self._redis_client.set(key, data, ex=timeout)
