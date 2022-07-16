"""
MedicalRegister Serializer 모듈
"""

__all__ = ["MedicalRegisterInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from iamdt.models import MedicalService
from iamdt_api.serializers.medical_service import MedicalServiceInfoSerializer


@extend_schema_serializer(component_name="MedicalRegisterInfo", examples=[])
class MedicalRegisterInfoSerializer(serializers.ModelSerializer):
    """진료접수번호 시리얼라이저

    진료내역을 단위별로 묶기 위해 있는 시리얼라이저.
    응답용으로만 사용된다.
    """

    stage = serializers.CharField(source="current_stage")  # 현재 단계 반환

    details = MedicalServiceInfoSerializer(many=True, read_only=True)  # 진료내역

    class Meta:
        model = MedicalService
        fields = [
            "id",
            "patient",
            "stage",
            "details",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "patient",
            "stage",
            "details",
            "created_at",
            "updated_at",
        ]
