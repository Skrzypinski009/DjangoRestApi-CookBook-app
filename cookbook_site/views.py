from rest_framework import (
    viewsets,
    generics,
    permissions,
)
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
    UserSerializer,
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


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()  # pyright: ignore
    serializer_class = IngredientSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()  # pyright: ignore
    serializer_class = RateSerializer

    def perform_create(self, serializer):
        recipe = serializer.validated_data["recipe"]
        Rate.objects.update_or_create(
            user=self.request.user,
            recipe=recipe,
            defaults={"stars": serializer.validated_data["stars"]},
        )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = (
        Recipe.objects.all()  # pyright: ignore
        .select_related("author")
        .prefetch_related("ingredients__ingredient")
        .annotate(average_rating=Coalesce(Avg("rates__stars"), Value(0.0)))
    )
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SavedRecipesViewSet(viewsets.ModelViewSet):
    queryset = SavedRecipes.objects.all()  # pyright: ignore
    serializer_class = SavedRecipesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]  # Każdy może założyć konto
    serializer_class = UserSerializer
