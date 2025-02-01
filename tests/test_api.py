from http import HTTPStatus

import pytest
import requests
from models.User import User


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    return response.json()["items"]

def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    users_list = response.json()["items"]
    for user in users_list:
        User.model_validate(user)


def test_users_not_duplicate(users):
    ids = [user["id"] for user in users]
    assert len(ids) == len(set(ids))

@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_none_exist_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "hello"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("size, page, expected_length", [
    (5, 1, 5),
    (5, 2, 5),
    (10, 1, 10),
    (3, 4, 3),
])
def test_pagination(app_url, size, page, expected_length):
    response = requests.get(f"{app_url}/api/users?size={size}&page={page}")
    assert response.status_code == HTTPStatus.OK

    user_data = response.json()
    items = user_data["items"]

    assert len(items) == expected_length
    assert user_data["total"] > 10

    if page > 1:
        previous_response = requests.get(f"{app_url}/api/users?size={size}&page={page - 1}")
        previous_user_data = previous_response.json()
        previous_items = previous_user_data["items"]
        current_ids = {user["id"] for user in items}
        previous_ids = {user["id"] for user in previous_items}
        assert current_ids.isdisjoint(previous_ids)