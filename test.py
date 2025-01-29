import requests
import pytest


@pytest.mark.parametrize("user_id, expected_email", [(2, "janet.weaver@reqres.in"),])
def test_user_data(user_id, expected_email):
    # url = f"https://reqres.in/api/users/{user_id}"
    url = f"http://0.0.0.0:8000/api/users/{user_id}"

    response = requests.get(url)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    body = response.json()
    assert "data" in body, "Response body does not contain 'data' key"
    data = body["data"]

    assert data["id"] == user_id, f"Expected id {user_id}, but got {data['id']}"
    assert data["email"] == expected_email, f"Expected email (expected_email), but got {data['email']}"


def test_user_not_found():
    # url = f"https://reqres.in/api/users/23"
    url = "http://0.0.0.0:8000/api/users/23"

    response = requests.get(url)
    assert response.status_code == 404, f"Response {response.status_code} {response.text}"


def test_create_user():
    # url = f"https://reqres.in/api/users"
    url = "http://0.0.0.0:8000/api/users"
    payload = {
        "name": "morpheus",
        "job": "leader"
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    body = response.json()
    assert body["name"] == "morpheus", f"Expected name 'morpheus', but got {body['name']}"
    assert body["job"] == "leader", f"Expected job 'leader', but got {body['job']}"
    assert body["id"] == int(body["id"]), f'Expected type of data, but came different from this'


def test_update_user():
    # url = f"https://reqres.in/api/users/2"
    url = f"http://0.0.0.0:8000/api/users/2"
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.put(url, json=payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    body = response.json()
    assert body["name"] == "morpheus", f"Expected name 'morpheus', but got {body['name']}"
    assert body["job"] == "zion resident", f"Expected job 'zion resident', but got {body['job']}"


def test_patched_user():
    # url = f"https://reqres.in/api/users/2"
    url = f"http://0.0.0.0:8000/api/users/2"
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.patch(url, json=payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    body = response.json()
    assert body["name"] == "morpheus", f"Expected name 'morpheus', but got {body['name']}"
    assert body["job"] == "zion resident", f"Expected job 'zion resident', but got {body['job']}"
