from tests.utils.factories import UserFactory
from bball_trainer.crud import user as crud_user
import pytest
from sqlalchemy.exc import SQLAlchemyError


def test_delete_user(session_db, test_client):
    db_user = UserFactory()
    response = test_client.delete(url=f"user/{db_user.id}")

    assert response.status_code == 204

    with pytest.raises(SQLAlchemyError) as cm:
        session_db.refresh(db_user)
    assert "Could not refresh instance" in str(cm.value)


def test_delete_user_unknown_id(test_client):
    response = test_client.delete(url="user/100")

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id."
