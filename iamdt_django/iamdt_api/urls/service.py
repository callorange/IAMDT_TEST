from django.urls import path


from ..views import service

app_name = "service"
urlpatterns = [
    # 인증
    path("services", service.MedicalServiceList.as_view(), name="list"),
    path("services/<int:id>", service.MedicalServiceDetail.as_view(), name="detail"),
]
