from typing import Any, Union, cast

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from bball_trainer import settings


def create_engine(url: Union[str, URL], pool_pre_ping: bool = True, **kwargs: Any) -> Engine:
    return sqlalchemy_create_engine(
        url=url,
        pool_pre_ping=pool_pre_ping,
        **kwargs,
    )


def create_session(bind: Engine) -> sessionmaker:
    """
    @see https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-sessionlocal-class
    """
    return sessionmaker(
        bind=bind,
        autocommit=False,  # For now, require explicit .commit() (default behavior)
        autoflush=False,  # For now, require explicit .flush() in transaction to see changes
    )


if settings.POSTGRES_URI is None:
    raise RuntimeError("Did you forgot to export POSTGRES_* env vars?")  # pragma: no cover

uri = cast(str, settings.POSTGRES_URI)
engine: Engine = create_engine(url=uri)

# Oneshot thread safe session (recommended)
SessionFactory: sessionmaker = create_session(bind=engine)
# *shared* session, so use it carefully (i.e: mainly testing)
SessionScoped: scoped_session = scoped_session(SessionFactory)
