from tests.utils.factories import GameRecordFactory, UserFactory
from bball_trainer.crud import game_record as crud_gr
from bball_trainer.schemas import GameRecordOut


def test_get_games(test_client):
    u = UserFactory(game=True)
    GameRecordFactory(user_id=u.id)
    GameRecordFactory(user_id=u.id)

    UserFactory(game=True)

    response = test_client.get(url=f"game_record/{u.id}/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3


def test_get_games_no_record(test_client):
    u = UserFactory()
    response = test_client.get(url=f"game_record/{u.id}/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 0


def test_get_games_unknown_id(test_client):
    response = test_client.get(url="game_record/100/")

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id."


def test_leaderboard(test_client):
    u_list = [UserFactory(game=True) for i in range(10)]

    GameRecordFactory(user_id=u_list[0].id, score=60)

    response = test_client.get(url="leaderboard/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 5
    assert data[0]["score"] == 60
    assert data[0]["user_id"] == u_list[0].id


def test_leaderboard_not_enough_games(test_client):
    u = UserFactory(game=True)
    GameRecordFactory(user_id=u.id, score=60)

    response = test_client.get(url="leaderboard/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["score"] == 60
    assert data[0]["user_id"] == u.id
