from tests.utils.factories import GameRecordFactory, UserFactory


def test_get_games(test_client):
    u = UserFactory(game=True)
    GameRecordFactory(user_id=u.id)
    last_game = GameRecordFactory(user_id=u.id)

    UserFactory(game=True)

    response = test_client.get(url=f"game_record/{u.id}/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    last_record = data[2]
    assert last_record["score"] == last_game.score
    assert last_record["user_id"] == last_game.user_id
    assert last_record["time"] == last_game.time
    assert last_record["difficulty"] == last_game.difficulty
    assert last_record.get("point_per_sec", 0) == last_game.point_per_sec
    assert last_record.get("id") == last_game.id
    assert last_record.get("created_at") == last_game.created_at.isoformat()


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

    g = GameRecordFactory(user_id=u_list[0].id, score=60, time=3)

    response = test_client.get(url="leaderboard/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 5
    assert data[0]["score"] == 60
    assert data[0]["user_id"] == u_list[0].id
    assert data[0]["time"] == 3
    assert data[0]["point_per_sec"] == 20
    assert data[0]["difficulty"] == g.difficulty


def test_leaderboard_not_enough_games(test_client):
    u = UserFactory(game=True)
    g = GameRecordFactory(user_id=u.id, score=60, time=1)

    response = test_client.get(url="leaderboard/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["score"] == 60
    assert data[0]["time"] == 1
    assert data[0]["point_per_sec"] == 60
    assert data[0]["difficulty"] == g.difficulty
    assert data[0]["user_id"] == u.id
