from bball_trainer.crud import game_record as crud_gr
from tests.utils.factories import UserFactory


def test_create_game(session_db, test_client):
    u = UserFactory()
    response = test_client.post(
        url="game_record/",
        json={"score": 10, "user_id": u.id},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["score"] == 10
    assert data["user_id"] == u.id
    assert data.get("id") is not None
    assert data.get("created_at") is not None

    db_gr = crud_gr.get_game(session_db, data["id"])
    assert db_gr.id
    assert db_gr.score == data["score"]
    assert db_gr.user_id == data["user_id"]
    assert db_gr.id == data["id"]
    assert db_gr.created_at.isoformat() == data["created_at"]


def test_create_user_missing_score(test_client):
    u = UserFactory()
    response = test_client.post(
        url="game_record/",
        json={"user_id": u.id},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


def test_create_user_missing_user_id(test_client):
    response = test_client.post(
        url="game_record/",
        json={"score": 11},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


def test_create_user_unknown_id(test_client):
    response = test_client.post(
        url="game_record/",
        json={"score": 12, "user_id": 100},
    )

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id, you can not create a game for it."
