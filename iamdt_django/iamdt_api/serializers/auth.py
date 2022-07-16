"""
인증 API 관련 Serializer 모듈
"""

__all__ = ["LoginSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from iamdt_api.scheme.auth import AUTH_API_EXAMPLES
from iamdt_api.scheme.staff import STAFF_API_EXAMPLES


@extend_schema_serializer(
    component_name="Login",
    examples=AUTH_API_EXAMPLES["add"] + STAFF_API_EXAMPLES["read"],
)
class LoginSerializer(serializers.Serializer):
    """로그인 요청 serializers"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
