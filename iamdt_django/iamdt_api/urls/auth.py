from django.urls import path


from ..views import auth

app_name = "auth"
urlpatterns = [
    # 인증
    path("auth/login", auth.Login.as_view(), name="login"),
    path("auth/logout", auth.Logout.as_view(), name="logout"),
]
