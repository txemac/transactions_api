from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_404_NOT_FOUND

from app import messages


def test_post_user_ok(client, data_user):
    response = client.post("/api/v1/users/", json=data_user)
    assert response.status_code == HTTP_201_CREATED


def test_post_user_name_already_exists(client, data_user):
    response = client.post("/api/v1/users/", json=data_user)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == messages.USER_NAME_ALREADY_EXISTS


def test_get_users(client, data_user):
    response = client.get("/api/v1/users/")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 1
    response_json = response.json()[0]
    assert response_json['name'] == data_user['name']
    assert response_json['email'] == data_user['email']
    assert response_json['age'] == data_user['age']


def test_get_user_by_name_ok(client, data_user):
    response = client.get(f"/api/v1/users/{data_user['name']}")
    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json['name'] == data_user['name']
    assert response_json['email'] == data_user['email']
    assert response_json['age'] == data_user['age']


def test_get_user_by_name_not_exists(client):
    response = client.get("/api/v1/users/not_exists")
    assert response.status_code == HTTP_404_NOT_FOUND
