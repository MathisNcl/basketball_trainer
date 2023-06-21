from bball_trainer.crud import game_record as crud_gr
from bball_trainer.crud import user as crud_user
from bball_trainer.models import GameRecord, User
from tests.utils.factories import UserFactory


def test_user(session_db):
    u = UserFactory(password="toto")

    with session_db as db:
        user = crud_user.get_user(db, id=u.id)

    assert isinstance(user, User)
    assert u.id == user.id
    assert u == user

    assert user.check_password("toto") is True
    assert user.check_password("tata") is False


def test_gamerecord(session_db):
    u = UserFactory(game=True)

    with session_db as db:
        game = crud_gr.get_game(db, id=u.id)

    assert isinstance(game, GameRecord)
    assert u.id == game.user_id

    assert isinstance(game.score, int)
    assert game.score >= 0
