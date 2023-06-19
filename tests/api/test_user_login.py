from tests.utils.factories import UserFactory


def test_login(test_client):
    # FIXME: Should use UserFactory instead
    test_client.post(
        url="user/",
        json={"pseudo": "localadmin", "password": "localadmin", "first_name": "dummy", "last_name": "dummy"},
    )
    response = test_client.post(
        url="user/login/",
        json={"pseudo": "localadmin", "password": "localadmin"},
    )

    assert response.status_code == 202
    data = response.json()
    assert data["pseudo"] == "localadmin"
    assert data["connected"]


def test_pseudo_unknown(test_client):
    response = test_client.post(
        url="user/login/",
        json={"pseudo": "dummy", "password": "password"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pseudo dummy does not exist."


def test_login_failed(test_client):
    u = UserFactory()
    response = test_client.post(
        url="user/login/",
        json={"pseudo": u.pseudo, "password": "password"},
    )

    assert response.status_code == 202

    data = response.json()

    assert data["pseudo"] == u.pseudo
    assert not (data["connected"])
