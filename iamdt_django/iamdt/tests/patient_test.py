__all__ = ["PatientModelTestCase"]

from django.test import TestCase
from django.core.exceptions import ValidationError

from iamdt.models import Customer, Patient
from iamdt.tests.customer_test import test_customer_info

test_patient_info = [
    {"name": "환자이름"},
    {"name": "환자이름"},
    {"name": "름이자환"},
    {"name": "환자이름"},
]


class PatientModelTestCase(TestCase):
    """
    환자 모델 테스트
    """

    def setUp(self) -> None:
        """고객을 외래키로 참조하므로 고객정보도 필요하다."""
        # 고객/환자 정보 생성
        for customer_info, patient_info in zip(test_customer_info, test_patient_info):
            customer = Customer.objects.create(**customer_info)
            Patient.objects.create(companion=customer, **patient_info)

    def test_info(self) -> None:
        """생성된 정보 확인"""
        customer_info = test_customer_info[0]
        patient_info = test_patient_info[0]
        customer = Customer.objects.get(
            name=customer_info["name"], phone=customer_info["phone"]
        )
        patient = Patient.objects.get(companion=customer, name=patient_info["name"])

        self.assertEqual(patient.name, patient_info["name"])  # 이름 확인
        self.assertEqual(patient.companion.name, customer_info["name"])  # 보호자 이름 확인

    def test_filter(self) -> None:
        """환자 모델 검색"""
        self.assertEqual(4, Patient.objects.all().count())  # 등록된 환자는 4명

    def test_filter_name(self) -> None:
        """환자 모델 이름 검색"""
        # 이름이 같은 환자는 3명
        self.assertEqual(3, Patient.objects.filter(name="환자이름").count())

    def test_validation_companion(self) -> None:
        """환자 모델 동행인 검증"""
        patient = Patient.objects.first()

        patient.companion = None
        with self.assertRaises(ValidationError):
            patient.full_clean()

    def test_validation_name(self) -> None:
        """환자 모델 이름 검증"""
        patient = Patient.objects.first()

        patient.name = ""
        with self.assertRaises(ValidationError):
            patient.full_clean()
