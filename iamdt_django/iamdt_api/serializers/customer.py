"""
Customer API 관련 Serializer 모듈
"""

__all__ = ["CustomerInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from iamdt.models import Customer
from iamdt_api.scheme.customer import CUSTOMER_API_EXAMPLES


@extend_schema_serializer(
    component_name="CustomerInfo",
    examples=CUSTOMER_API_EXAMPLES["all"],
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
