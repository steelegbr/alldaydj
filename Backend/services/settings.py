from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_audience: str
    jwt_algorithm: str
    jwt_client_id: str
    jwt_domain: str
    jwt_issuer: str
    mongodb_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
