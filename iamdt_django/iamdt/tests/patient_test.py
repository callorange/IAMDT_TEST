__all__ = ["PatientModelTestCase"]

from django.test import TestCase
from django.core.exceptions import ValidationError

from iamdt.models import Customer, Patient


class PatientModelTestCase(TestCase):
    """
    환자 모델 테스트
    """

    fixtures = ["user.json", "customer.json", "patient.json"]

    def setUp(self) -> None:
        """고객을 외래키로 참조하므로 고객정보도 필요하다."""
        self.customer_data = {"name": "고객", "phone": "01011112222"}
        self.patient_data = {"name": "같은이름"}

    def test_info(self) -> None:
        """생성된 정보 확인"""
        customer = Customer.objects.get(**self.customer_data)
        patient = Patient.objects.get(
            companion=customer, name=self.patient_data["name"]
        )

        self.assertEqual(patient.name, self.patient_data["name"])  # 이름 확인
        self.assertEqual(
            patient.companion.name, self.customer_data["name"]
        )  # 보호자 이름 확인

    def test_filter(self) -> None:
        """환자 모델 검색"""
        # 미리등록된 5
        self.assertEqual(5, Patient.objects.all().count())

    def test_filter_name(self) -> None:
        """환자 모델 이름 검색"""
        # 이름이 같은 환자는 2명
        self.assertEqual(2, Patient.objects.filter(name="같은이름").count())

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
