"""
API 검색 설정을 위한 FilterSet 모듈
"""

__all__ = ["MedicalRegisterFilter"]


from django_filters import rest_framework as filters

from iamdt.models import MedicalRegister


class MedicalRegisterFilter(filters.FilterSet):
    """의료 서비스 내역 검색 필터"""

    patient = filters.CharFilter(field_name="patient__name", lookup_expr="icontains")

    class Meta:
        model = MedicalRegister
        exclude = ["patient", "created_at", "updated_at"]
