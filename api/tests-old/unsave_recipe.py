import requests
from login import login_interface


class DeleteError(Exception):
    pass


BASE_URL = f"http://127.0.0.1:8000/api/recipes"


def unsave_recipe(token, recipe_id):
    url = f"{BASE_URL}/{recipe_id}/unsave/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(url, headers=headers)

    if response.status_code != 204:
        raise DeleteError


def main():
    token = login_interface()
    if token == None:
        return

    try:
        unsave_recipe(token, 2)
        print("Save delete: SUCCESS")

    except DeleteError:
        print("Save delete: ERROR")


if __name__ == "__main__":
    main()
