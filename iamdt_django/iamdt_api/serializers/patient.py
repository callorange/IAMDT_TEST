"""
Patient Serializer 모듈
"""

__all__ = ["PatientInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from iamdt.models import Patient


class PatientInfoSerializer(serializers.ModelSerializer):
    """환자정보 시리얼라이저"""

    pass
