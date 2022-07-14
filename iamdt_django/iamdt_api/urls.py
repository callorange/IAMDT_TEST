from django.urls import path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import auth

app_name = "api"
urlpatterns = [
    # 인증
    path("auth/login", auth.Login.as_view(), name="login"),
    path("auth/logout", auth.Logout.as_view(), name="logout"),
    # Documentation: DRF Spectacular
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger",
    ),
    path(
        "schema/redoc",
        SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
]
