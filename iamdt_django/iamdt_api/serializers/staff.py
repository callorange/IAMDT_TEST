"""
Staff API 관련 Serializer 모듈
"""

__all__ = ["StaffAddSerializer", "StaffInfoSerializer"]

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from iamdt_api.scheme.staff import staff_api_examples


@extend_schema_serializer(component_name="StaffAdd", examples=staff_api_examples["add"])
class StaffAddSerializer(serializers.ModelSerializer):
    """스태프 등록을 위한 시리얼라이저

    username, password, phone는 필수
    password는 등록할때만
    role은 지정되지 않은경우 doctor로 등록 됩니다.
    """

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
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
