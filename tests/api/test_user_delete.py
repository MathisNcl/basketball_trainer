import pytest
from sqlalchemy.exc import SQLAlchemyError

from bball_trainer.crud import game_record as crud_gr
from tests.utils.factories import GameRecordFactory, UserFactory


def test_delete_user(session_db, test_client):
    db_user = UserFactory(game=True)
    user_id = db_user.id
    GameRecordFactory(user_id=user_id)

    response = test_client.delete(url=f"user/{user_id}/")

    assert response.status_code == 204

    with pytest.raises(SQLAlchemyError) as cm:
        session_db.refresh(db_user)
    assert "Could not refresh instance" in str(cm.value)

    games = crud_gr.get_all_games_user(db=session_db, user_id=user_id)
    assert len(games) == 0


def test_delete_user_unknown_id(test_client):
    response = test_client.delete(url="user/100/")

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id."
