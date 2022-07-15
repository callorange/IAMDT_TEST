"""
Staff API 관련 Serializer 모듈
"""

__all__ = [
    "StaffAddSerializer",
    "StaffInfoSerializer",
    "SimpleStaffInfoSerializer",
    "SimpleStaffField",
]


from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
    extend_schema_field,
)
from rest_framework import serializers

from iamdt_api.scheme.staff import staff_api_examples


@extend_schema_serializer(component_name="StaffAdd", examples=staff_api_examples["add"])
class StaffAddSerializer(serializers.ModelSerializer):
    """스태프 등록을 위한 시리얼라이저

    username, password, phone는 필수
    password는 등록할때만
    role은 지정되지 않은경우 doctor로 등록 됩니다.
    """

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
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
        read_only_fields = ["id", "is_staff", "is_superuser"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


@extend_schema_serializer(
    component_name="StaffInfo", examples=staff_api_examples["mod"]
)
class StaffInfoSerializer(serializers.ModelSerializer):
    """스태프 정보 시리얼라이저"""

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


@extend_schema_serializer(
    component_name="SimpleStaffInfo",
    examples=[
        OpenApiExample(
            name="스태프 최소 정보",
            summary="스태프(병원관계자) 최소 정보",
            description="스태프(병원관계자)의 최소한의 정보만 출력 됩니다.",
            value={
                "id": 2,
                "username": "doctor2",
                "first_name": "name2",
                "last_name": "doc",
            },
            response_only=True,
        )
    ],
)
class SimpleStaffInfoSerializer(serializers.ModelSerializer):
    """스태프 최소 정보 시리얼라이저"""

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "role_display",
        ]
        read_only_fields = ["id", "username", "first_name", "last_name"]


@extend_schema_field(SimpleStaffInfoSerializer)
class SimpleStaffField(serializers.PrimaryKeyRelatedField):
    """유저 참조 필드를 위한 PrimaryKeyRelatedField

    Response시 SimpleStaffSerializer를
    Request시 int 값으로 받기 위한 필드 객체다.

    nested serializer로 구현되면 Staff 테이블에 작업(등록/수정)이 된다
    """

    def to_representation(self, value):
        # super().to_representation(value)
        return SimpleStaffInfoSerializer(value).data
