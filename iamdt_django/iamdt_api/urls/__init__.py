from django.urls import path, include

app_name = "api"
urlpatterns = [
    # 인증
    path("", include("iamdt_api.urls.auth")),
    # 스태프
    path("", include("iamdt_api.urls.staff")),
    # Documentation: DRF Spectacular
    path("", include("iamdt_api.urls.doc")),
]
