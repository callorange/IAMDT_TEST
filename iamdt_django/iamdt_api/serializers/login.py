"""
인증 API 관련 Serializer 모듈
"""

__all__ = ["LoginSerializer"]

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """로그인 요청 serializers"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
