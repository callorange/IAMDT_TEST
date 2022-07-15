"""
인증 API 관련 Serializer 모듈
"""

__all__ = ["LoginSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from iamdt_api.scheme.auth import auth_api_examples
from iamdt_api.scheme.staff import staff_api_examples


@extend_schema_serializer(
    component_name="Login",
    examples=auth_api_examples["add"] + staff_api_examples["read"],
)
class LoginSerializer(serializers.Serializer):
    """로그인 요청 serializers"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
