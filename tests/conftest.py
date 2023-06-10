import pytest
from typing import Generator
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from bball_trainer.models import Base

from bball_trainer.models.database import SessionScoped
from bball_trainer import settings

from tests.utils.db import configure_sessionmakers, init_db


@pytest.fixture
def hand() -> dict:
    return {
        "lmList": [
            [139, 460, 0],
            [226, 437, -27],
            [304, 362, -29],
            [350, 290, -30],
            [368, 226, -31],
            [286, 269, -6],
            [336, 199, -25],
            [364, 158, -43],
            [386, 121, -56],
            [233, 245, -7],
            [274, 166, -19],
            [301, 118, -35],
            [326, 81, -48],
            [174, 236, -13],
            [210, 156, -28],
            [240, 112, -39],
            [271, 80, -48],
            [110, 240, -22],
            [133, 167, -39],
            [161, 128, -44],
            [195, 102, -47],
        ],
        "bbox": (110, 80, 276, 380),
        "center": (248, 270),
        "type": "Right",
    }


@pytest.fixture
def config_point() -> dict:
    return {
        "xfrom1": 50,
        "xto1": 200,
        "xfrom2": 300,
        "xto2": 450,
        "yfrom": 50,
        "yto": 450,
    }


@pytest.fixture(scope="session", autouse=True)
def test_engine() -> Generator[Engine, None, None]:
    test_db_name: str = f"test_{settings.POSTGRES_DBNAME}"

    init_db(test_db_name)
    test_engine: Engine = configure_sessionmakers(test_db_name)

    yield test_engine


@pytest.fixture
def session_db(test_engine) -> Generator[Session, None, None]:
    """
    On a small project, it doesn't really matter if we create/drop
    all tables PER EACH test methods...
    Of course, on a biggest project, it would be quickly a REAL bottleneck!
    """
    Base.metadata.create_all(bind=test_engine)
    session_db: Session = SessionScoped()

    yield session_db

    SessionScoped.remove()
    Base.metadata.drop_all(bind=test_engine)
