from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DBNAME: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str = "localhost"

    POSTGRES_URI: Optional[str]

    LANGUAGE_CODE: str = "fr-FR"

    @validator("POSTGRES_URI", pre=True)
    def assemble_db(cls, v: Optional[str], values: dict[str, Any]) -> str:
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            path=f"/{values.get('POSTGRES_DBNAME') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
