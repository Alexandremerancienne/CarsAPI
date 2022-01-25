from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from .views import (
    CarViewSet,
    CustomUserViewSet,
    CarBrandViewSet,
    CarModelViewSet,
    ChangePasswordView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter()
router.register("cars", CarViewSet, basename="cars")
router.register("users", CustomUserViewSet, basename="users")
router.register("brands", CarBrandViewSet, basename="brands")
router.register("models", CarModelViewSet, basename="models")

urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", include("dj_rest_auth.registration.urls")),
    path("change_password/", ChangePasswordView.as_view(), name="change-password"),
]
