from typing import Generator
from unittest.mock import MagicMock

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from bball_trainer import settings
from bball_trainer.api.main import app
from bball_trainer.models import Base
from bball_trainer.models.database import SessionScoped
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
def two_hands() -> list:
    return [
        {
            "lmList": [
                [1050, 425, 0],
                [1015, 402, -8],
                [992, 368, -13],
                [977, 338, -17],
                [960, 320, -22],
                [1016, 341, -12],
                [1010, 302, -22],
                [1009, 278, -29],
                [1009, 258, -34],
                [1040, 339, -15],
                [1040, 296, -24],
                [1041, 269, -31],
                [1042, 247, -35],
                [1063, 344, -20],
                [1071, 304, -30],
                [1075, 279, -36],
                [1078, 258, -41],
                [1085, 354, -25],
                [1097, 323, -35],
                [1105, 303, -38],
                [1111, 285, -40],
            ],
            "bbox": (960, 247, 151, 178),
            "center": (1035, 336),
            "type": "Right",
        },
        {
            "lmList": [
                [216, 452, 0],
                [248, 430, -15],
                [274, 399, -23],
                [298, 374, -31],
                [322, 361, -40],
                [248, 359, -21],
                [258, 319, -33],
                [261, 294, -42],
                [262, 273, -50],
                [223, 357, -24],
                [227, 314, -35],
                [228, 286, -44],
                [227, 263, -52],
                [199, 364, -28],
                [195, 324, -40],
                [192, 298, -49],
                [190, 277, -56],
                [177, 380, -33],
                [157, 352, -46],
                [144, 334, -52],
                [135, 317, -56],
            ],
            "bbox": (135, 263, 187, 189),
            "center": (228, 357),
            "type": "Left",
        },
    ]


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


@pytest.fixture
def test_client(session_db) -> TestClient:
    yield TestClient(app)


@pytest.fixture
def disable_authentication(monkeypatch):
    basic_auth_mock = MagicMock()
    monkeypatch.setattr("dash_auth.BasicAuth", basic_auth_mock)

    basic_auth_mock.return_value.is_authorized.return_value = True

    yield
