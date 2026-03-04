import requests
from login import login_interface

BASE_URL = "http://127.0.0.1:8000/api/rates/"


# You cannot specify the user (private rates).
def get_rates(token, params={}):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        print("Get Rates: SUCCESS")
        return response.json()
    else:
        print("Get Rates: ERROR")
        print(f"Status code: {response.status_code}")


def main():
    token = login_interface()
    if token == None:
        return

    rates = get_rates(token, {"recipe": 2})
    print(rates)


if __name__ == "__main__":
    main()
