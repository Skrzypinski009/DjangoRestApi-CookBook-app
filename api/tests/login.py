import requests

BASE_URL = "http://127.0.0.1:8000/api"
users = [
    {
        "username": "testuser_1",
        "password": "StrongPassword123!",
        "email": "test1@example.com",
        "first_name": "Jan",
        "last_name": "Kowalski",
    },
    {
        "username": "testuser_2",
        "password": "StrongPassword123!",
        "email": "test2@example.com",
        "first_name": "Adam",
        "last_name": "Stopa",
    },
    {
        "username": "testuser_3",
        "password": "StrongPassword123!",
        "email": "test3@example.com",
        "first_name": "Janusz",
        "last_name": "Nowak",
    },
]


def get_user_data(idx: int):
    try:
        return users[idx - 1]
    except:
        print("Wrong index!")
        print(f"Index has to be in range: 1 - {len(users)}")
        return None


def login(user_data):
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


def login_user(idx):
    user_data = get_user_data(idx)
    if user_data == None:
        return None

    token = login(user_data)
    return token


def register(user_data):
    register_url = f"{BASE_URL}/register/"
    response = requests.post(register_url, json=user_data)
    if response.status_code == 201:
        print("Register: SUCCESS")
        return True
    else:
        print("Register: ERROR")
        print(f"Status code: {response.status_code}")
        return False


def register_all():
    for user in users:
        register(user)


def get_my_data(token) -> dict | None:
    headers = {"Authorization": f"Token {token}"}
    me_url = f"{BASE_URL}/me"
    response = requests.get(me_url, headers=headers)
    if response.status_code == 200:
        print(f"Get user: SUCCESS")
        return response.json()
    else:
        print(f"Get user: ERROR")
        print(f"Status code: {response.status_code}")
        return None


def user_action_interface(action):
    print("select user:")

    for idx, user in enumerate(users):
        print(f"{idx+1}. {user['username']} ({user['first_name']}{user['last_name']})")

    try:
        choice = int(input(": "))
        user = users[choice - 1]
    except:
        print("Wrong input!")
        exit()

    return action(user)


def login_interface():
    return user_action_interface(login)


def register_interface():
    return user_action_interface(register)


def main():
    actions = [register, login]

    print("Choose action:")
    print("1. Register")
    print("2. Login")
    try:
        choice = int(input(": "))
        action = actions[choice - 1]
    except:
        print("Wrong input!")
        exit()

    user_action_interface(action)


if __name__ == "__main__":
    main()
