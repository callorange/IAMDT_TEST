from django.urls import path


from ..views import patient

app_name = "patient"
urlpatterns = [
    # 인증
    path("patients", patient.PatientList.as_view(), name="list"),
    path("patients/<int:id>", patient.PatientDetail.as_view(), name="detail"),
]
