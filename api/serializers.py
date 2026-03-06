from rest_framework import fields, serializers
from django.db import transaction
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

    def validate(self, attrs):
        data = super().validate(attrs)
        instance = self.instance

        recipe = data.get("recipe", instance.recipe if instance else None)
        user = self.context["request"].user

        if recipe.author == user:
            raise serializers.ValidationError("You cannot rate your recipes!")

        if instance and "recipe" in data and data["recipe"] != instance.recipe:
            raise serializers.ValidationError(
                {"recipe": "You can't change recipe of that rate!"}
            )

        return data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ["name", "amount"]

    def to_representation(self, instance):
        return {
            "name": instance.ingredient.name,
            "amount": instance.amount,
        }


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
    # Author data is taken from request
    author = UserSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "author",
            "ingredients",
            "instructions",
            "average_rating",
            "image",
        ]

    def create(self, validated_data):
        print(validated_data)
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)

        for data in ingredients_data:
            print(data)
            ingredient_obj, _ = Ingredient.objects.get_or_create(
                name=data["name"],
            )

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                amount=data["amount"],
                # unit=data["unit"],
            )

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", None)
        instance = super().update(instance, validated_data)

        relations = []

        if ingredients_data is not None:
            with transaction.atomic():
                instance.ingredients.all().delete()

                for ing in ingredients_data:
                    ing_obj = Ingredient.objects.get_or_create(
                        name=Ingredient.name_normalize(ing["name"]),
                    )

                    relations.append(
                        RecipeIngredient(
                            recipe=instance,
                            ingredient=ing_obj,
                            amount=ing["amount"],
                        )
                    )

                RecipeIngredient.objects.bulk_create(relations)

        return instance


class SavedRecipesSerializer(serializers.ModelSerializer):
    # recipe_details = RecipeSerializer(source="recipe", read_only=True)

    class Meta:
        model = SavedRecipes
        fields = ["user", "recipe"]
