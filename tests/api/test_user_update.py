from tests.utils.factories import UserFactory
import pytest


def test_update_user_unknown(test_client):
    response = test_client.patch(url="user/100", json={})

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "100 is not a known id."


@pytest.mark.parametrize(
    "attribute, old_value, new_value",
    [
        ("last_name", "old", "Dummy"),
        ("first_name", "old", "Dummy"),
        ("age", 18, 19),
    ],
)
def test_update_user(test_client, session_db, attribute, old_value, new_value):
    u = UserFactory(**{attribute: old_value})
    response = test_client.patch(url=f"user/{u.id}", json={attribute: new_value})

    assert response.status_code == 200

    data = response.json()
    session_db.refresh(u)
    assert data[attribute] == new_value
    assert getattr(u, attribute) == new_value


def test_update_password(test_client, session_db):
    u = UserFactory(password="old_password")
    response = test_client.patch(url=f"user/{u.id}", json={"password": "new_password"})

    assert response.status_code == 200

    session_db.refresh(u)
    assert u.check_password("new_password")
