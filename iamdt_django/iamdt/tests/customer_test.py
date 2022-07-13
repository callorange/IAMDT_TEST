__all__ = ["CustomerModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Customer

test_customer_info = [
    {"name": "고객", "phone": "01011112222"},
    {"name": "고객2", "phone": "01033334444"},
    {"name": "고객3", "phone": "01055556666"},
    {"name": "고객", "phone": "01077778888"},
]


class CustomerModelTestCase(TestCase):
    """
    고객 모델 테스트
    """

    fixtures = ["user.json", "customer.json"]

    def setUp(self) -> None:
        # 고객 정보 생성
        for customer_info in test_customer_info:
            Customer.objects.create(**customer_info)

    def test_unique_constraint(self) -> None:
        """고객정보는 복합키(연락처+이름)를 사용하므로 해당 정보 확인"""
        with self.assertRaises(Exception):
            Customer.objects.create(**test_customer_info[0])

    def test_info(self) -> None:
        """생성된 정보 확인"""
        customer_info = test_customer_info[0]
        customer = Customer.objects.get(
            name=customer_info["name"], phone=customer_info["phone"]
        )

        # 이름 확인
        self.assertEqual(customer.name, customer_info["name"])

        # 연락처 확인
        self.assertEqual(customer.phone, customer_info["phone"])

    def test_filter(self) -> None:
        """고객 모델 검색"""
        # 생성된 고객수는 4명
        self.assertEqual(4, Customer.objects.all().count())

    def test_filter_name(self) -> None:
        """고객 모델 이름 검색"""
        # 이름이 같은 고객은 2명
        self.assertEqual(2, Customer.objects.filter(name="고객").count())

    def test_filter_phone(self) -> None:
        """고객 모델 이름 검색"""
        # 전화번호는 중복이 없다.
        self.assertEqual(1, Customer.objects.filter(phone="01011112222").count())

    def test_validation_name(self) -> None:
        """고객 정보 이름 검증"""
        customer = Customer.objects.first()

        customer.name = ""
        with self.assertRaises(ValidationError):
            customer.full_clean()

        customer.name = None
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_validation_phone(self) -> None:
        """고객 정보 연락처 검증"""
        customer = Customer.objects.first()

        customer.phone = "ㅁㅁㅁㅁ"
        with self.assertRaises(ValidationError):
            customer.full_clean()

        customer.phone = "00012341234"
        with self.assertRaises(ValidationError):
            customer.full_clean()

        customer.phone = None
        with self.assertRaises(ValidationError):
            customer.full_clean()

        customer.phone = ""
        with self.assertRaises(ValidationError):
            customer.full_clean()
