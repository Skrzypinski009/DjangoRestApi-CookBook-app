import requests

BASE_URL = "http://127.0.0.1:8000/api"

user_data = {
    "username": "testuser_1",
    "password": "StrongPassword123!",
    "email": "test@example.com",
    "first_name": "Jan",
    "last_name": "Kowalski",
}


def login():
    login_url = f"{BASE_URL}/login/"
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"],
    }
    response = requests.post(login_url, json=login_data)

    if response.status_code == 200:
        token = response.json().get("token")
        print("Login: SUCCESS")
        print(f"Login Token: {token}")
        return token
    else:
        print("Login: ERROR")
        print(f"Status code: {response.status_code}")
        return None


def register():
    register_url = f"{BASE_URL}/register/"
    response = requests.post(register_url, json=user_data)
    if response.status_code == 201:
        print("Register: SUCCESS")
        return True
    else:
        print("Register: ERROR")
        print(f"Status code: {response.status_code}")
        return False


def get_user(token):
    headers = {"Authorization": f"Token {token}"}
    me_url = f"{BASE_URL}/me"
    response = requests.get(me_url, headers=headers)
    if response.status_code == 200:
        print(f"Get user: SUCCESS")
        return response.json()
    else:
        print(f"Get user: ERROR")
        print(f"Status code: {response.status_code}")


def main():
    avaliable_actions = [1, 2]
    choice = 0
    while choice not in avaliable_actions:
        print("Choose action:")
        print("1. Register")
        print("2. Login")
        try:
            choice = int(input("choice"))
        except:
            pass

    match choice:
        case 1:
            register()
        case 2:
            login()


if __name__ == "__main__":
    main()
