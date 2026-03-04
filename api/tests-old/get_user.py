import requests

URL = "http://127.0.0.1:8000/api/me/"


def get_user(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        print("Get user: SUCCESS")
        return response.json()
    else:
        print("Get user: ERROR")
        print(f"Status code: {response.status_code}")
        return None
