from functools import lru_cache

from cathouse.core.config import Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()
