from rest_framework import fields, serializers
from django.contrib.auth.models import User
from .models import (
    Ingredient,
    Rate,
    Recipe,
    RecipeIngredient,
    SavedRecipes,
    SavedRecipes,
)


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ["id", "recipe", "stars"]
        read_only_fields = ["user"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="ingredient.name")

    class Meta:
        model = RecipeIngredient
        fields = ["name", "amount"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    author = UserSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "author",
            "instructions",
            "image",
            "ingredients",
            "average_rating",
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)

        for data in ingredients_data:
            ingredient_obj, _ = Ingredient.objects.get_or_create(name=data["name"])

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                amount=data["amount"],
                unit=data["unit"],
            )

        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class SavedRecipesSerializer(serializers.ModelSerializer):
    recipe_details = RecipeSerializer(source="recipe", read_only=True)

    class Meta:
        model = SavedRecipes
        fields = ["user", "recipe", "recipe_details"]
        read_only_fields = ["user"]
