from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Recipe, Ingredient, RecipeIngredient


class RecipeAPITest(APITestCase):
    def setUp(self):
        self.setUp_auth()
        self.setUp_recipes()

    def setUp_auth(self):
        self.user = User.objects.create(username="tester", password="123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp_recipes(self):
        ing, _ = Ingredient.objects.get_or_create(name="egg")

        self.recipes = []
        for i in range(12):
            recipe = Recipe.objects.create(
                title="Eggs " + str(i + 1),
                description="Delicious.",
                author=self.user,
                instructions="Cook",
                image=None,
            )
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ing,
                amount=5,
            )
            self.recipes.append(recipe)

    def test_api_recpe_get(self):
        url = reverse("api:recipe-list")

        response = self.client.get(url)
        response2 = self.client.get(url, data={"page": "2"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(response.json()["count"], 12)

        # pagination test
        results = response.json()["results"]
        results2 = response2.json()["results"]

        self.assertEqual(len(results), 10)
        self.assertEqual(len(results2), 2)

    def test_api_recipe_get_by_author(self):
        other_user = User.objects.create(username="other", password="123")
        url = reverse("api:recipe-list")

        data = {"author": self.user.id}
        data2 = {"author": other_user.id}

        response = self.client.get(url, data=data)
        response2 = self.client.get(url, data=data2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        results = response.json()["results"]
        results2 = response2.json()["results"]

        self.assertEqual(len(results), 10)
        self.assertEqual(len(results2), 0)

    def test_api_recipe_create(self):
        url = reverse("api:recipe-list")
        data = {
            "title": "Eggs",
            "description": "Delicious.",
            "instructions": "Cook",
            "ingredients": [
                {"name": "egg", "amount": 2},
                {"name": "beacon", "amount": 20},
            ],
        }

        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, 201)

        recipe_id = response.json()["id"]
        recipe = Recipe.objects.get(id=recipe_id)

        ing_count = len(RecipeIngredient.objects.filter(recipe=recipe))
        self.assertEqual(ing_count, 2)

    def test_api_recipe_update_image(self):
        image_content = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9"
            b"\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00"
            b"\x00\x02\x02\x44\x01\x00\x3b"
        )

        image = SimpleUploadedFile(
            name="image.jpg",
            content=image_content,
            content_type="image/jpeg",
        )

        recipe = self.recipes[0]
        url = reverse("api:recipe-detail", kwargs={"pk": recipe.id})
        data = {"image": image}
        response = self.client.patch(url, data=data, format="multipart")

        self.assertEqual(response.status_code, 200)

    def test_api_recipe_save_unsave(self):
        self.recipe_save()
        count = self.recipe_get_saved()
        self.assertEqual(count, 1)

        self.recipe_unsave()
        count = self.recipe_get_saved()
        self.assertEqual(count, 0)

    def recipe_save(self):
        url = reverse("api:recipe-save", kwargs={"pk": 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def recipe_get_saved(self):
        url = reverse("api:recipe-saved")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return len(response.json())

    def recipe_unsave(self):
        url = reverse("api:recipe-unsave", kwargs={"pk": 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
