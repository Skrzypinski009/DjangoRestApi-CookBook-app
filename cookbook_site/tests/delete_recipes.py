import requests
from login import get_user, login
from get_recipes import get_user_recipes


def delete_user_recipes(token, recipes_ids):
    headers = {"Authorization": f"Token {token}"}
    for r_id in recipes_ids:
        del_url = f"http://127.0.0.1:8000/api/recipes/{r_id}/"
        response = requests.delete(del_url, headers=headers)

        if response.status_code == 204:
            print(f"Recipe [{r_id}] delete: SUCCESS")
        else:
            print(f"Recipe [{r_id}] delete: ERROR")
            print(f"Status code: {response.status_code}")


def main():
    token = login()
    if not token:
        return

    user_data = get_user(token)
    if not user_data:
        return

    recipes = get_user_recipes(token, user_data["id"])
    if not recipes:
        return

    recipes_ids = [r["id"] for r in recipes["results"]]
    delete_user_recipes(token, recipes_ids)


if __name__ == "__main__":
    main()
