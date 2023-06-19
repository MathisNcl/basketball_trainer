from tests.utils.factories import UserFactory


def test_get_users(test_client):
    UserFactory()
    UserFactory()
    response = test_client.get(url="user/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2


def test_get_user(test_client):
    u = UserFactory()
    response = test_client.get(url=f"user/{u.id}/")

    assert response.status_code == 200

    data = response.json()
    assert data["pseudo"] == u.pseudo
    assert data["last_name"] == u.last_name
    assert data["first_name"] == u.first_name
    assert data["age"] == u.age


def test_get_user_unknow_id(test_client):
    response = test_client.get(url="user/100/")

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id."
