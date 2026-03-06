from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from api.models import Recipe, Rate


class RateAPITest(APITestCase):
    def setUp(self):
        self.setUp_auth()
        self.setUp_objects()

    def setUp_auth(self):
        self.user = User.objects.create_user(
            username="tester",
            password="123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp_objects(self):
        self.other_user = User.objects.create_user(
            username="other",
            password="123",
        )
        self.user_recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            author=self.user,
            instructions="Test Instructions",
            image=None,
        )
        self.other_user_recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            author=self.other_user,
            instructions="Test Instructions",
            image=None,
        )
        self.other_user_rate = Rate.objects.create(
            recipe=self.user_recipe,
            user=self.other_user,
            stars=2,
        )
        self.user_rate = Rate.objects.create(
            recipe=self.other_user_recipe,
            user=self.user,
            stars=3,
        )

    def test_api_rate_get_all(self):
        url = reverse("api:rate-list")
        response = self.client.get(url)
        results = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 2)

    def test_api_rate_get_by_recipe(self):
        url = reverse("api:rate-list")
        data = {"recipe": self.user_recipe.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)

        results = response.json()
        self.assertEqual(len(results), 1)

    def test_api_rate_cant_create_for_own_recipe(self):
        url = reverse("api:rate-list")
        data = {
            "recipe": self.user_recipe.id,
            "stars": 3,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_rate_create_for_other_recipe(self):
        url = reverse("api:rate-list")
        data = {
            "recipe": self.other_user_recipe.id,
            "stars": 3,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_api_rate_delete_own(self):
        url = reverse("api:rate-detail", kwargs={"pk": self.user_rate.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_api_rate_cant_delete_other(self):
        url = reverse("api:rate-detail", kwargs={"pk": self.other_user_rate.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_api_rate_update_own(self):
        url = reverse("api:rate-detail", kwargs={"pk": self.user_rate.id})
        data = {"stars": 5}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)

        stars = response.json()["stars"]
        self.assertEqual(stars, 5)

    def test_api_rate_cant_update_other(self):
        url = reverse("api:rate-detail", kwargs={"pk": self.other_user_rate.id})
        data = {"stars": 5}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 403)
