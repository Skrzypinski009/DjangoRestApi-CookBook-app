import requests
from login import login_interface

BASE_URL = "http://127.0.0.1:8000/api/ingredients"


def get_ingredients(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(BASE_URL, headers=headers)

    if response.status_code == 200:
        print("Get Recipes: SUCCESS")
        return response.json()
    else:
        print("Get Recipes: ERROR")
        print(f"Status code: {response.status_code}")


def main():
    token = login_interface()
    if token == None:
        return

    ingredients = get_ingredients(token)
    print(ingredients)


if __name__ == "__main__":
    main()
