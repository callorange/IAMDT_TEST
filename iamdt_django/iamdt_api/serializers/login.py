"""
인증 API 관련 Serializer 모듈
"""

__all__ = ["LoginSerializer"]

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="로그인 성공",
            summary="로그인 요청 성공",
            description="로그인 요청시 제출 되어야 하는 데이터 입니다.",
            value={"username": "doctor1", "password": "doc12345678"},
            request_only=True,
        ),
        OpenApiExample(
            name="로그인 실패",
            summary="로그인 요청 실패",
            description="로그인 요청이 실패하는 데이터",
            value={"username": "doctor1"},
            request_only=True,
        ),
    ],
)
class LoginSerializer(serializers.Serializer):
    """로그인 요청 serializers"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
