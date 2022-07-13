__all__ = ["IAMDTCustomerModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Customer

test_customer_info = [
    {"customer_name": "고객1", "phone": "01011112222", "email": "customer@customer.com"},
    {"customer_name": "고객2", "phone": "01033334444", "email": "customer@customer.com"},
    {"customer_name": "고객3", "phone": "01055556666", "email": "customer@customer.com"},
    {"customer_name": "고객4", "phone": "01077778888", "email": "customer@customer.com"},
]


class IAMDTCustomerModelTestCase(TestCase):
    """
    고객 모델 테스트
    """

    def setUp(self) -> None:
        # 고객 정보 생성
        for customer_info in test_customer_info:
            Customer.objects.create(**customer_info)

    def test_customer_info(self):
        """생성된 정보 확인"""
        customer_info = test_customer_info[0]
        customer = Customer.objects.get(phone=customer_info["phone"])

        # 연락처 확인
        self.assertEqual(customer.phone, customer_info["phone"])

        # 이름 확인
        self.assertEqual(customer.customer_name, customer_info["customer_name"])

    def test_unique_constraint(self):
        """고객정보는 복합키(연락처+이름)를 사용하므로 해당 정보 확인"""
        with self.assertRaises(ValidationError):
            Customer.objects.create(**test_customer_info[0])
