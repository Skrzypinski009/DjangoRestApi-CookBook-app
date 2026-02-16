from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RecipeViewSet, IngredientViewSet, RateViewSet, RegisterView

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet)
router.register(r"ingredients", IngredientViewSet)
router.register(r"rates", RateViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", obtain_auth_token, name="login"),
]
