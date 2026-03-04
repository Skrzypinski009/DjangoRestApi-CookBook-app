import requests
from login import login_interface

BASE_URL = f"http://127.0.0.1:8000/api/recipes"


def save_recipe(token, recipe_id):
    url = f"{BASE_URL}/{recipe_id}/save/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(url, headers=headers)

    if response.status_code == 201:
        print("Save create: SUCCESS")
        return response.json()
    else:
        print("Save create: ERROR")
        print(f"Status code: {response.status_code}")
        return None


def main():
    token = login_interface()
    if token == None:
        return

    save = save_recipe(token, 2)
    if save == None:
        return

    print(save)


if __name__ == "__main__":
    main()
