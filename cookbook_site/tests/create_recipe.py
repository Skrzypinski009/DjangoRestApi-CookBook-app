import requests
from login import login

BASE_URL = "http://127.0.0.1:8000/api"


def create_recipe(headers):

    recipe_payload = {
        "title": "Pyszna Jajecznica",
        "description": "Klasyczne śniadanie",
        "instructions": "Rozbij jajka, smaż na maśle przez 5 minut.",
        "ingredients": [
            {"name": "Jajka", "amount": 3, "unit": "szt"},
            {"name": "Masło", "amount": 10, "unit": "g"},
        ],
    }
    recipe_url = f"{BASE_URL}/recipes/"

    response = requests.post(recipe_url, json=recipe_payload, headers=headers)

    if response.status_code == 201:
        print("Recipe create: SUCCESS")
        return response.json()
    else:
        print("Recipe create: ERROR")
        print(f"Status code: {response.status_code}")
        return None


def upload_image(recipe_id, headers):
    recipe_url = f"{BASE_URL}/recipes/{recipe_id}/"

    with open("img.jpg", "rb") as image_file:
        files = {"image": image_file}
        response = requests.patch(recipe_url, files=files, headers=headers)
        if response.status_code == 200:
            print("Image upload: SUCCESS")
            return response.json()
        else:
            print("Image upload: ERROR")
            print(f"Status code: {response.status_code}")
            return None


def main():
    token = login()
    if token == None:
        return

    headers = {"Authorization": f"Token {token}"}

    recipe = create_recipe(headers)
    if recipe == None:
        return

    print(recipe)

    image = upload_image(recipe["id"], headers)
    if image == None:
        return

    print(image)


if __name__ == "__main__":
    main()
