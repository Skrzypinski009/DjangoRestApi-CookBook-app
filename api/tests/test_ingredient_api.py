from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User


class IngredientAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="123")
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_ingredients(self):
        url = reverse("api:ingredient-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_ingredients_not_allowed(self):
        url = reverse("api:ingredient-list")
        data = {"name": "tomato"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 405)
