from django.urls import path


from ..views import staff

app_name = "staff"
urlpatterns = [
    # 인증
    path("staffs", staff.StaffList.as_view(), name="list"),
    path("staffs/<int:id>", staff.StaffDetail.as_view(), name="detail"),
]
