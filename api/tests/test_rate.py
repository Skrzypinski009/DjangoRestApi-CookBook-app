from django.db.utils import IntegrityError
from django.test import TestCase
from api.models import Rate, Recipe
from django.contrib.auth.models import User


class RateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="walt", password="123")
        self.recipe = Recipe.objects.create(
            title="Beans",
            description="Delicious beans.",
            author=self.user,
            instructions="Do nothing.",
            image=None,
        )
        self.rate = Rate.objects.create(
            user=self.user,
            recipe=self.recipe,
            stars=3,
        )

    def test_does_not_duplicate_rate(self):
        with self.assertRaises(IntegrityError):
            Rate.objects.create(
                user=self.user,
                recipe=self.recipe,
                stars=1,
            )

    def test_change_rate_stars_value(self):
        self.rate.stars = 5
        self.rate.save()

        self.assertEqual(self.rate.stars, 5)
