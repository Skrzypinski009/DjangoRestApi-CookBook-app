import requests

URL_ME = "http://127.0.0.1:8000/api/me/"
TOKEN = "TWÓJ_TOKEN"
headers = {"Authorization": f"Token {TOKEN}"}

response = requests.get(URL_ME, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    my_id = user_data["id"]
    print(f"Moje ID to: {my_id}")
    print(f"Zalogowany jako: {user_data['username']}")
else:
    print("Nie udało się pobrać danych użytkownika.")
