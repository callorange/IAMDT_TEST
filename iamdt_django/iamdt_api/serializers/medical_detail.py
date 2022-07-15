"""
MedicalDetail Serializer 모듈
"""

__all__ = ["MedicalDetailInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from iamdt.models import MedicalDetail


@extend_schema_serializer(component_name="MedicalDetailInfo", examples=[])
class MedicalDetailInfoSerializer(serializers.ModelSerializer):
    """환자정보 시리얼라이저"""

    class Meta:
        model = MedicalDetail
        fields = [
            "id",
            "register",
            "stage",
            "status",
            "creator",
            "staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "creator", "created_at", "updated_at"]
