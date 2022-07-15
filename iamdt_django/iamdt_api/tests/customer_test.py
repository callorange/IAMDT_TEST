__all__ = ["CustomerSerialiezerTestCase"]


from django.test import TestCase

from iamdt.models import Customer
from iamdt_api.serializers import CustomerInfoSerializer


class CustomerSerialiezerTestCase(TestCase):
    """
    고객 시리얼라이저 테스트
    """

    fixtures = ["user.json", "customer.json"]

    def setUp(self) -> None:
        self.customer_obj = Customer.objects.get(id=1)
        self.customer_dict = {"name": "고객1", "phone": "01011112222"}

    def test_serializer(self) -> None:
        """고객 객체가 주어졌을때"""
        serializer = CustomerInfoSerializer(self.customer_obj)
        self.assertEqual("고객1", serializer.data["name"])

        serializer = CustomerInfoSerializer(
            self.customer_obj, data={"phone": "01099999999"}, partial=True
        )
        serializer.is_valid()
        self.assertEqual("01099999999", serializer.validated_data["phone"])

    def test_validation_name(self) -> None:
        """이름 validation"""
        # blank
        self.customer_dict["name"] = ""
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # null
        self.customer_dict["name"] = None
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # missing
        self.customer_dict.pop("name")
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

    def test_validation_phone(self) -> None:
        """연락처 validation"""
        # regex
        self.customer_dict["phone"] = "11122223333"
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # blank
        self.customer_dict["phone"] = ""
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # null
        self.customer_dict["phone"] = None
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # missing
        self.customer_dict.pop("phone")
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

    def test_validation_unique(self) -> None:
        """이름+연락처 복합키를 사용하므로 중복 X"""
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())
