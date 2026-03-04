import requests
from login import login_interface

BASE_URL = f"http://127.0.0.1:8000/api/recipes/saved/"


def get_saved(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(BASE_URL, headers=headers)

    if response.status_code == 200:
        print("Get Saved: SUCCESS")
        return response.json()
    else:
        print("Get Saved: ERROR")
        print(response.status_code)
        return None


def main():
    token = login_interface()
    if token == None:
        return

    saved = get_saved(token)
    if saved == None:
        return

    print(saved)


if __name__ == "__main__":
    main()
