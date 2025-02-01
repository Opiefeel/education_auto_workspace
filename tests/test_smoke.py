# для проверки жив ли сайт
from http import HTTPStatus

import requests

def test_smoke_status(app_url):
    response = requests.get(f"{app_url}/api/status")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["users"] is True

def test_smoke_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK