"""
Patient Serializer 모듈
"""

__all__ = ["PatientInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from iamdt.models import Patient
from iamdt_api.scheme.patient import PATIENT_API_EXAMPLES


@extend_schema_serializer(
    component_name="PatientInfo", examples=PATIENT_API_EXAMPLES["all"]
)
class PatientInfoSerializer(serializers.ModelSerializer):
    """환자정보 시리얼라이저"""

    class Meta:
        model = Patient
        fields = ["id", "name", "companion", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        validators = [
            UniqueTogetherValidator(
                queryset=Patient.objects.all(), fields=["companion", "name"]
            )
        ]
