__all__ = ["RegistrationModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Customer, Patient
from iamdt.models.register import Register
from iamdt.models.choices import MedicalStage

stage_names = [
    "REGISTER",
    "EXAMINATION",
    "DIAGNOSYS",
    "TREATMENT",
    "COUNSELING",
    "PAYMENT",
    "DISCHARGE",
]
stage_values = [
    "register",
    "examination",
    "diagnosys",
    "treatment",
    "counseling",
    "payment",
    "discharge",
]
stage_labels = ["접수", "진료", "진단", "처치", "결과 설명/상담", "수납", "퇴원"]


class MedicalStageChoicesTestCase(TestCase):
    """
    진료 단계 choices 클래스 테스트
    """

    fixtures = ["user.json", "customer.json", "patient.json", "register.json"]

    def setUp(self):
        pass

    def test_stage(self) -> None:
        """Role 종류 Choices 확인"""
        self.assertEqual(stage_names, MedicalStage.names)
        self.assertEqual(stage_values, MedicalStage.values)
        self.assertEqual(stage_labels, MedicalStage.labels)


class RegistrationModelTestCase(TestCase):
    """진료 접수 모델 테스트"""

    fixtures = ["user.json", "customer.json", "patient.json", "register.json"]

    def setUp(self) -> None:
        """접수시 환자/고객 정보가 모두 필요하다"""
        # 환자 {"pk":5,"companion": 4,"name": "환자5"}
        self.patient = Patient.objects.last()

        # 접수 {"id":1"patient": 1,"stage": "discharge"}
        self.register = Register.objects.first()

    def test_info(self) -> None:
        """생성된 정보 확인"""
        self.assertEqual(self.register.patient, Patient.objects.get(id=1))
        self.assertEqual(self.register.stage, MedicalStage.DISCHARGE)

    def test_filter(self) -> None:
        """진료 접수 모델 검색"""
        self.assertEqual(6, Register.objects.all().count())

    def test_filter_patient(self) -> None:
        """진료 접수 모델 검색"""
        # 환자1 의 최근 접수 id는 2
        self.assertEqual(2, Register.objects.filter(patient=1).last().id)
        # 환자5 의 접수 id는 6
        self.assertEqual(6, Register.objects.filter(patient=self.patient).last().id)

    def test_validation_patient(self):
        """진료 접수 환자 검증"""
        with self.assertRaises(ValidationError):
            self.register.patient = None
            self.register.full_clean()

        with self.assertRaises(ValueError):
            self.register.patient = 9999

    def test_validation_stage(self):
        """진료 접수 단계 검증"""
        with self.assertRaises(ValidationError):
            self.register.stage = None
            self.register.full_clean()

        with self.assertRaises(ValidationError):
            self.register.stage = ""
            self.register.full_clean()

        with self.assertRaises(ValidationError):
            self.register.stage = "asdf"
            self.register.full_clean()

        self.register.stage = MedicalStage.EXAMINATION
        self.register.full_clean()
        self.register.save()
        self.register.refresh_from_db()
        self.assertEqual(self.register.stage, MedicalStage.EXAMINATION)
