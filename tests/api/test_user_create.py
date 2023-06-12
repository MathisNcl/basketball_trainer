from bball_trainer.crud import user as crud_user
import pytest


def test_create_user(session_db, test_client):
    response = test_client.post(
        url="user/",
        json={"pseudo": "Captain", "last_name": "Nicoli", "first_name": "Mathis", "age": 25, "password": "blabla"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["pseudo"] == "Captain"
    assert data["last_name"] == "Nicoli"
    assert data["first_name"] == "Mathis"
    assert data["age"] == 25
    assert data.get("id") is not None
    assert "password" not in data

    db_user = crud_user.get_user(session_db, data["id"])
    assert db_user.id
    assert db_user.pseudo == data["pseudo"]
    assert db_user.last_name == data["last_name"]
    assert db_user.first_name == data["first_name"]
    assert db_user.age == data["age"]

    assert db_user.check_password("blabla") == True


@pytest.mark.parametrize(
    "attribute_missing, expected_status",
    [
        ("pseudo", 422),
        ("last_name", 422),
        ("first_name", 422),
        ("password", 422),
        ("age", 201),
    ],
)
def test_create_user_missing_infos(session_db, test_client, attribute_missing, expected_status):
    json_dict = {"pseudo": "Captain", "last_name": "Nicoli", "first_name": "Mathis", "age": 25, "password": "blabla"}
    del json_dict[attribute_missing]

    response = test_client.post(
        url="user/",
        json=json_dict,
    )

    assert response.status_code == expected_status
