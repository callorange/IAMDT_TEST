"""
MedicalDetail Serializer 모듈
"""

__all__ = ["MedicalServiceInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from iamdt.models import MedicalService


@extend_schema_serializer(component_name="MedicalDetailInfo", examples=[])
class MedicalServiceInfoSerializer(serializers.ModelSerializer):
    """환자정보 시리얼라이저"""

    class Meta:
        model = MedicalService
        fields = [
            "id",
            "patient",
            "register",
            "stage",
            "status",
            "creator",
            "staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "creator", "created_at", "updated_at"]
