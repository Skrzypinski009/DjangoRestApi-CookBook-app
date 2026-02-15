from rest_framework import viewsets
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from cookbook_site.serializer import (
    IngredientSerializer,
    RateSerializer,
    RecipeSerializer,
    RecipeIngredientSerializer,
    SavedRecipesSerializer,
)
from .models import (
    Ingredient,
    Rate,
    Recipe,
    RecipeIngredient,
    SavedRecipes,
    SavedRecipes,
)
from .paginations import RecipePagination


class IngredientVeiwSet(viewsets.ViewSet):
    queryset = Ingredient.objects.all()  # pyright: ignore
    serializer_class = Ingredient


class RateViewSet(viewsets.ViewSet):
    queryset = Rate.objects.all()  # pyright: ignore
    serializer_class = RateSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = (
        Recipe.objects.all()  # pyright: ignore
        .select_related("author")
        .prefetch_related("ingredients__ingredient")
        .annotate(average_rating=Coalesce(Avg("rates__stars"), Value(0.0)))
    )
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination


class SavedRecipesViewSet(viewsets.ViewSet):
    queryset = SavedRecipes.objects.all()  # pyright: ignore
    serializer_class = SavedRecipesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]
