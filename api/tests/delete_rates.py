import requests
from login import get_my_data, login_interface
from get_rates import get_rates


def delete_user_rates(token, rates_ids):
    headers = {"Authorization": f"Token {token}"}
    for r_id in rates_ids:
        del_url = f"http://127.0.0.1:8000/api/rates/{r_id}/"
        response = requests.delete(del_url, headers=headers)

        if response.status_code == 204:
            print(f"Rate [{r_id}] delete: SUCCESS")
        else:
            print(f"Rate [{r_id}] delete: ERROR")
            print(f"Status code: {response.status_code}")


def main():
    token = login_interface()
    if not token:
        return

    user_data = get_my_data(token)
    if not user_data:
        return

    rates = get_rates(token)
    if not rates:
        return

    rates_ids = [r["id"] for r in rates]
    delete_user_rates(token, rates_ids)


if __name__ == "__main__":
    main()
