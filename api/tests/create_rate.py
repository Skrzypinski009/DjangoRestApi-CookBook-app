import requests
from login import login_interface

URL = "http://127.0.0.1:8000/api/rates/"


def create_rate(token):
    rate_payload = {
        "recipe": 2,
        "stars": 3,
    }
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(URL, json=rate_payload, headers=headers)

    if response.status_code == 201:
        print("Rate create: SUCCESS")
        return response.json()
    else:
        print("Rate create: ERROR")
        print(f"Status code: {response.status_code}")
        return None


def main():
    token = login_interface()
    if token == None:
        return

    rate = create_rate(token)
    if rate == None:
        return


if __name__ == "__main__":
    main()
