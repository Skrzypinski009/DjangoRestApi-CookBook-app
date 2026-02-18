from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import (
    viewsets,
    generics,
    permissions,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from .serializers import (
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
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly


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
    # JSON for default data
    # MultiPart for image
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        author_id = self.request.query_params.get("author")

        if author_id is not None:
            qs = qs.filter(author_id=author_id)
        return qs


class SavedRecipesViewSet(viewsets.ModelViewSet):
    queryset = SavedRecipes.objects.all()  # pyright: ignore
    serializer_class = SavedRecipesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]  # Każdy może założyć konto
    serializer_class = UserSerializer


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        }
        return Response(user_data)
