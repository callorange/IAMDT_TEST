__all__ = ["CustomerModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Customer


class CustomerModelTestCase(TestCase):
    """
    고객 모델 테스트
    """

    fixtures = ["user.json", "customer.json"]

    def setUp(self) -> None:
        self.customer1_info = {"name": "고객1", "phone": "01011112222"}
        self.customer5_info = {"name": "고객5", "phone": "01055556666"}
        Customer.objects.create(**self.customer5_info)

    def test_unique_constraint(self) -> None:
        """고객정보는 복합키(연락처+이름)를 사용하므로 해당 정보 확인"""
        with self.assertRaises(Exception):
            Customer.objects.create(**self.customer1_info)

    def test_info(self) -> None:
        """생성된 정보 확인"""
        customer = Customer.objects.get(
            name=self.customer1_info["name"], phone=self.customer1_info["phone"]
        )

        # 이름 확인
        self.assertEqual(customer.name, self.customer1_info["name"])

        # 연락처 확인
        self.assertEqual(customer.phone, self.customer1_info["phone"])

    def test_filter(self) -> None:
        """고객 모델 검색"""
        # 생성된 고객수는 4 + 1
        self.assertEqual(5, Customer.objects.all().count())

    def test_filter_name(self) -> None:
        """고객 모델 이름 검색"""
        self.assertEqual(0, Customer.objects.filter(name="고객").count())
        self.assertEqual(1, Customer.objects.filter(name="고객1").count())
        self.assertEqual(5, Customer.objects.filter(name__contains="고객").count())

    def test_filter_phone(self) -> None:
        """고객 모델 이름 검색"""
        self.assertEqual(0, Customer.objects.filter(phone="01055555555").count())
        self.assertEqual(1, Customer.objects.filter(phone="01011112222").count())
        self.assertEqual(2, Customer.objects.filter(phone="01055556666").count())
        self.assertEqual(2, Customer.objects.filter(phone__contains="2222").count())

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
