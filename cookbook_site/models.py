from django.db import models
from django.db.models import (
    ForeignKey,
    ManyToManyField,
    CharField,
    TextField,
    IntegerField,
    FloatField,
    ImageField,
)
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = CharField(max_length=40)
    description = TextField(max_length=250)
    author = ForeignKey(User, on_delete=models.CASCADE)
    instructions = TextField(max_length=400)
    image = ImageField("recipe_img/", blank=True, null=True)


class Rate(models.Model):
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE, related_name="rates")
    stars = IntegerField()
    user = ForeignKey(User, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = CharField(max_length=25, unique=True)


class RecipeIngredient(models.Model):
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = FloatField()


class SavedRecipes(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "recipe")
