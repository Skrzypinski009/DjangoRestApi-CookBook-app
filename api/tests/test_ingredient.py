from django.db.utils import IntegrityError
from django.test import TestCase
from api.models import Ingredient


class IngredientTest(TestCase):
    def setUp(self):
        Ingredient.objects.create(name="peper")
        Ingredient.objects.create(name="sugar")

    def test_names_of_exising_ingredients(self):
        ingredients = Ingredient.objects.all()
        self.assertEqual(len(ingredients), 2)

        names = set([i.name for i in ingredients])
        self.assertEqual(names, {"peper", "sugar"})

    def test_get_or_create_does_not_duplicate_ingredient(self):
        _, created = Ingredient.objects.get_or_create(name="peper")
        self.assertFalse(created)

    def test_create_does_not_duplicate_ingredient(self):
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name="peper")

    def test_update_does_not_duplicate_ingredient(self):
        sugar = Ingredient.objects.get(name="sugar")
        sugar.name = "peper"

        with self.assertRaises(IntegrityError):
            sugar.save()
