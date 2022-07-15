"""
Customer API 관련 Serializer 모듈
"""

__all__ = ["CustomerInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from iamdt.models import Customer


@extend_schema_serializer(
    component_name="CustomerInfo",
    examples=[
        OpenApiExample(
            name="고객 추가",
            summary="고객정보 신규 등록",
            description="고객정보를 추가한다. 이름+연락처 결과는 중복될 수 없다.",
            value={"name": "customer1", "phone": "01022223333"},
            request_only=True,
        ),
        OpenApiExample(
            name="고객 추가 실패",
            summary="고객정보 신규 등록 실패",
            description="이름과 연락처는 모두 필수 값이며, 연락처는 핸드폰 형식에 맞춰 입력되어야 한다.",
            value={"name": "customer1", "phone": "11122223333"},
            request_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="고객 정보 조회",
            summary="고객 정보 조회",
            description="고객정보 조회시에는 read_only 필드인 id, created_at, updated_at이 포함된다",
            value={
                "id": "1",
                "name": "고객1",
                "phone": "01022223333",
                "created_at": "2022-07-13T10:28:31.680Z",
                "updated_at": "2022-07-13T10:30:21.885Z",
            },
            response_only=True,
            external_value="asdfasdflkjqwl;ekfjql;wekf",
        ),
        OpenApiExample(
            name="고객 정보 추가/수정",
            summary="고객 정보 추가/수정 결과",
            description="고객정보 추가/수정시 read_only 필드인 id, created_at, updated_at이 제외된다",
            value={"name": "고객1", "phone": "01022223333"},
            response_only=True,
        ),
    ],
)
class CustomerInfoSerializer(serializers.ModelSerializer):
    """고객정보 시리얼라이저"""

    class Meta:
        model = Customer
        fields = ["id", "name", "phone", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        validators = [
            UniqueTogetherValidator(
                queryset=Customer.objects.all(), fields=["name", "phone"]
            )
        ]
