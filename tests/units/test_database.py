from tests.utils.factories import UserFactory
from bball_trainer.crud import user as crud_user
from bball_trainer.models import User


def test_user(session_db):
    u = UserFactory()

    with session_db as db:
        user = crud_user.get_user(db, u.id)

    assert isinstance(user, User)
    assert u.id == user.id
