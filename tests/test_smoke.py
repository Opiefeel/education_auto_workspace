# для проверки жив ли сайт

import requests

def test_smoke(app_url):
    response = requests.get("{app_url}/api/status")
