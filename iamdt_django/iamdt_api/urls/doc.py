from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

app_name = "doc"
urlpatterns = [
    path("doc/scheme", SpectacularAPIView.as_view(), name="scheme"),
    path(
        "doc/swagger",
        SpectacularSwaggerView.as_view(url_name="api:doc:scheme"),
        name="swagger",
    ),
    path(
        "doc/redoc",
        SpectacularRedocView.as_view(url_name="api:doc:scheme"),
        name="redoc",
    ),
]
