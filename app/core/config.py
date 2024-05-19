from typing import Any, Optional

from pydantic import Field, PostgresDsn, validator
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("Ultimate FastAPI Project Setup")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("postgres", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int | str = Field("5432", env="POSTGRES_PORT")
    POSTGRES_ECHO: bool = Field(False, env="POSTGRES_ECHO")
    POSTGRES_POOL_SIZE: int = Field(10, env="POSTGRES_POOL_SIZE")
    ASYNC_POSTGRES_URI: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"

    @validator("ASYNC_POSTGRES_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
