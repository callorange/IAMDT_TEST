__all__ = ["MedicalRegisterModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Patient
from iamdt.models.medical_register import MedicalRegister
from iamdt.models.choices import MedicalStage


class MedicalRegisterModelTestCase(TestCase):
    """진료 접수 모델 테스트"""

    fixtures = ["user.json", "customer.json", "patient.json", "medical_register.json"]

    def setUp(self) -> None:
        """접수시 환자/고객 정보가 모두 필요하다"""
        # 환자 {"pk":5,"companion": 4,"name": "환자5"}
        self.patient = Patient.objects.last()

        # 접수 {"id":1"patient": 1,"stage": "discharge"}
        self.register = MedicalRegister.objects.first()

    def test_info(self) -> None:
        """생성된 정보 확인"""
        self.assertEqual(self.register.patient, Patient.objects.get(id=1))

    def test_filter(self) -> None:
        """진료 접수 모델 검색"""
        self.assertEqual(6, MedicalRegister.objects.all().count())

    def test_filter_patient(self) -> None:
        """진료 접수 모델 검색"""
        # 환자1 의 최근 접수 id는 2
        self.assertEqual(2, MedicalRegister.objects.filter(patient=1).last().id)
        # 환자5 의 접수 id는 6
        self.assertEqual(
            6, MedicalRegister.objects.filter(patient=self.patient).last().id
        )

    def test_validation_patient(self):
        """진료 접수 환자 검증"""
        with self.assertRaises(ValidationError):
            self.register.patient = None
            self.register.full_clean()

        with self.assertRaises(ValueError):
            self.register.patient = 9999
