import requests
from pprint import pprint
from login import login

BASE_URL = "http://127.0.0.1:8000/api/recipes/"


def get_recipes(token, params={}):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        print("Get Recipes: SUCCESS")
        return response.json()
    else:
        print("Get Recipes: ERROR")
        print(f"Status code: {response.status_code}")


def get_user_recipes(token, user_id):
    return get_recipes(token, {"author": user_id})


def main():
    token = login()
    if not token:
        return

    recipes = get_recipes(token)
    if not recipes:
        return

    print(f"Pobrano {len(recipes['results'])} przepisów:\n")
    pprint(recipes, indent=4, width=100)


if __name__ == "__main__":
    main()
