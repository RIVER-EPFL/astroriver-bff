from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_REALM: str
    KEYCLOAK_URL: str

    # SOIL-API settings
    SOIL_API_URL: str  # Full path to the Soil API (eg: http://soil-api-dev)


@lru_cache()
def get_config():
    return Config()


config = get_config()
