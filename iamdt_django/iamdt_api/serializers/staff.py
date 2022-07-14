"""
Staff API 관련 Serializer 모듈
"""

__all__ = [
    "StaffSerializer",
]

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="스태프 등록",
            summary="스태프(병원관계자) 정보 등록",
            description="스태프(병원관계자)의 정보 등록/수정 예제",
            value={
                "username": "doctor2",
                "first_name": "name2",
                "last_name": "doc",
                "role": "doctor",
                "phone": "01012345678",
                "messenger": "kakaotalk",
                "messenger_id": "doc2",
            },
            request_only=True,
        ),
        OpenApiExample(
            name="스태프 조회",
            summary="스태프(병원관계자) 정보 조회",
            description="스태프(병원관계자)의 정보 조회 예제",
            value={
                "id": 2,
                "username": "doctor1",
                "first_name": "name1",
                "last_name": "doc",
                "role": "doctor",
                "role_display": "수의사",
                "phone": "01012345678",
                "messenger": "kakaotalk",
                "messenger_id": "doc1",
            },
            response_only=True,
        ),
    ],
)
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
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = ["id", "username", "is_staff", "is_superuser"]
