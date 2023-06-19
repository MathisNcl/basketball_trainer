from tests.utils.factories import GameRecordFactory, UserFactory


def test_get_games(test_client):
    u = UserFactory(game=True)
    GameRecordFactory(user_id=u.id)
    GameRecordFactory(user_id=u.id)

    UserFactory(game=True)

    response = test_client.get(url=f"game_record/{u.id}")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3


def test_get_games_no_record(test_client):
    u = UserFactory()
    response = test_client.get(url=f"game_record/{u.id}")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 0


def test_get_games_unknown_id(test_client):
    response = test_client.get(url="game_record/100")

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id."
