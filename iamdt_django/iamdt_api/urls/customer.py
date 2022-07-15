from django.urls import path


from ..views import customer

app_name = "staff"
urlpatterns = [
    # 인증
    path("customers", customer.CustomerList.as_view(), name="list"),
    path("customers/<int:id>", customer.CustomerDetail.as_view(), name="detail"),
]
