import sys
from pathlib import Path
from typing import Any, Optional, cast

from pydantic import BaseSettings, PostgresDsn, validator

PACKAGE_DIR: Path = Path(cast(str, sys.modules["bball_trainer"].__file__)).parent
BASE_DIR: Path = PACKAGE_DIR.parent.parent if PACKAGE_DIR.parent.name == "src" else PACKAGE_DIR


class Settings(BaseSettings):
    PACKAGE_DIR: Path = PACKAGE_DIR

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
        env_file = [BASE_DIR / ".env"]
        env_file_encoding = "utf-8"
