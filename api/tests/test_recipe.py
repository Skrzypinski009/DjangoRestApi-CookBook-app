from django.db.utils import IntegrityError
from django.test import TestCase
from api.models import Recipe, Ingredient, RecipeIngredient, SavedRecipes
from django.contrib.auth.models import User


class RecipeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="123")
        self.recipe = Recipe.objects.create(
            title="Steak",
            description="Delicious stake.",
            author=self.user,
            instructions="Add salt to steak and frie on both sides.",
            image=None,
        )
        SavedRecipes.objects.create(user=self.user, recipe=self.recipe)

    def test_add_ingredients(self):
        ing1, _ = Ingredient.objects.get_or_create(name="steak")
        ing2, _ = Ingredient.objects.get_or_create(name="salt")

        RecipeIngredient.objects.create(
            ingredient=ing1,
            recipe=self.recipe,
            amount=1,
        )
        RecipeIngredient.objects.create(
            ingredient=ing2,
            recipe=self.recipe,
            amount=50,
        )

        recipe_ings = self.recipe.ingredients.all()
        self.assertEqual(len(recipe_ings), 2)

        ings_names = set([ri.ingredient.name for ri in recipe_ings])
        self.assertEqual(ings_names, {"steak", "salt"})

    def test_does_not_duplicate_saved_recipe(self):
        with self.assertRaises(IntegrityError):
            SavedRecipes.objects.create(user=self.user, recipe=self.recipe)

    def test_get_saved_recipes(self):
        saved = list(SavedRecipes.objects.filter(user=self.user))
        saved_recipes = set([s.recipe for s in saved])
        self.assertEqual(saved_recipes, {self.recipe})
