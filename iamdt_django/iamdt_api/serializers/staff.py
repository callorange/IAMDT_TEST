"""
Staff API 관련 Serializer 모듈
"""

__all__ = ["StaffAddSerializer", "StaffInfoSerializer"]

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers


@extend_schema_serializer(
    component_name="StaffAdd",
    examples=[
        OpenApiExample(
            name="스태프 등록",
            summary="스태프(병원관계자) 정보 등록",
            description="스태프(병원관계자)의 정보 등록<br>role을 지정하지 않으면 doctor로 기본 지정됨",
            value={
                "username": "doctor2",
                "password": "123123",
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
            name="스태프 등록 실패",
            summary="스태프(병원관계자) 정보 등록 실패",
            description="스태프(병원관계자)의 정보 등록 실패를 테스트를 위한 예제",
            value={"username": "doctor2"},
            request_only=True,
        ),
        OpenApiExample(
            name="스태프 등록 결과",
            summary="스태프(병원관계자) 정보 등록 결과",
            description="스태프(병원관계자)의 정보 등록 결과",
            value={
                "username": "doctor2",
                "first_name": "name2",
                "last_name": "doc",
                "role": "doctor",
                "phone": "01012345678",
                "messenger": "kakaotalk",
                "messenger_id": "doc2",
            },
            response_only=True,
        ),
    ],
)
class StaffAddSerializer(serializers.ModelSerializer):
    """스태프 등록을 위한 시리얼라이저

    username, password, phone는 필수
    password는 등록할때만
    role은 지정되지 않은경우 doctor로 등록 됩니다.
    """

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
            "phone",
            "messenger",
            "messenger_id",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


@extend_schema_serializer(
    component_name="StaffInfo",
    examples=[
        OpenApiExample(
            name="스태프 정보 수정",
            summary="스태프(병원관계자) 정보 수정-성공",
            description="스태프(병원관계자)의 정보 수정 성공. role과 messenger의 choices value 선택에 주의",
            value={
                "first_name": "name1",
                "last_name": "doc",
                "role": "doctor",
                "phone": "01012345678",
                "messenger": "kakaotalk",
                "messenger_id": "doc1",
            },
            request_only=True,
        ),
        OpenApiExample(
            name="스태프 정보 수정 실패",
            summary="스태프(병원관계자) 정보 수정 실패",
            description="스태프(병원관계자)의 정보 수정 실패 예제. 핸드폰 번호는 비워둘 수 없다",
            value={
                "first_name": "name1",
                "last_name": "doc",
                "role": "doctor",
                "phone": "",
                "messenger": "kakaotalk",
                "messenger_id": "doc1",
            },
            request_only=True,
        ),
        OpenApiExample(
            name="스태프 정보",
            summary="스태프(병원관계자) 정보 조회/수정 결과",
            description="스태프(병원관계자)의 정보 조회/수정 결과",
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
                "is_staff": True,
                "is_superuser": False,
            },
            response_only=True,
        ),
    ],
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
