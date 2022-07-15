"""
API 검색 설정을 위한 FilterSet 모듈
"""

__all__ = ["MedicalRegisterFilter", "StaffFilter"]

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from iamdt.models import MedicalRegister


class MedicalRegisterFilter(filters.FilterSet):
    """의료 서비스 내역 검색 필터"""

    patient = filters.CharFilter(field_name="patient__name", lookup_expr="icontains")

    class Meta:
        model = MedicalRegister
        fields = []


class StaffFilter(filters.FilterSet):
    """스태프 검색 필터"""

    username = filters.CharFilter(field_name="username", lookup_expr="icontains")
    role = filters.ChoiceFilter(choices=get_user_model().UserType.choices)
    phone = filters.CharFilter(field_name="phone", lookup_expr="icontains")

    o = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("username", "username"),
            ("role", "role"),
            ("created_at", "created_at"),
        ),
        # labels do not need to retain order
        field_labels={
            "username": "User account",
        },
    )

    class Meta:
        model = get_user_model()
        fields = []
