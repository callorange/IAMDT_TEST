"""
Staff API 관련 Serializer 모듈
"""

__all__ = [
    "StaffSerializer",
]

from django.contrib.auth import get_user_model
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    """django user serializer"""

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "role",
            "role_display",
            "phone",
            "messenger",
            "messenger_id",
        ]
        read_only_fields = [
            "id",
            "username",
        ]
