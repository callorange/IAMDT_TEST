__all__ = ["MedicalStageStatusChoicesTestCase", "MedicalDetailModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Patient, MedicalRegister
from iamdt.models.choices import MedicalStageStatus, MedicalStage
from iamdt.models.medical_service import MedicalService


class MedicalStageChoicesTestCase(TestCase):
    """
    진료 단계 choices 클래스 테스트
    """

    def setUp(self):
        pass

    def test_stage_names(self) -> None:
        """Choices name 확인"""
        stage_names = [
            "REGISTER",
            "EXAMINATION",
            "DIAGNOSYS",
            "TREATMENT",
            "COUNSELING",
            "PAYMENT",
            "DISCHARGE",
        ]
        self.assertEqual(stage_names, MedicalStage.names)

    def test_stage_values(self) -> None:
        """Choices value 확인"""
        stage_values = [
            "register",
            "examination",
            "diagnosys",
            "treatment",
            "counseling",
            "payment",
            "discharge",
        ]
        self.assertEqual(stage_values, MedicalStage.values)

    def test_stage_labels(self) -> None:
        """Choices label 확인"""
        stage_labels = ["접수", "진료", "진단", "처치", "결과 설명/상담", "수납", "퇴원"]
        self.assertEqual(stage_labels, MedicalStage.labels)


class MedicalStageStatusChoicesTestCase(TestCase):
    """진료 단계 상태(대기/완료) choices 테스트"""

    def setUp(self):
        pass

    def test_status_names(self) -> None:
        """MedicalStageStatus Choices name 테스트"""
        names = ["WAIT", "COMPLETE"]
        self.assertEqual(names, MedicalStageStatus.names)

    def test_status_values(self) -> None:
        """MedicalStageStatus Choices value 테스트"""
        values = ["wait", "complete"]
        self.assertEqual(values, MedicalStageStatus.values)

    def test_status_labels(self) -> None:
        """MedicalStageStatus Choices label 테스트"""
        labels = ["대기", "완료"]
        self.assertEqual(labels, MedicalStageStatus.labels)


class MedicalDetailModelTestCase(TestCase):
    """진료 내역 모델 테스트"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_service.json",
    ]

    def setUp(self) -> None:
        self.last = MedicalService.objects.last()

    def test_filter_patient(self) -> None:
        """환자 진료 내역 필터링"""
        patient = Patient.objects.get(id=1)
        count = MedicalService.objects.filter(patient=patient).count()
        self.assertEqual(6, count)

    def test_filter_register(self) -> None:
        """환자 접수 단위 내역 필터링"""
        register = MedicalRegister.objects.get(id=1)
        count = MedicalService.objects.filter(register=register).count()
        self.assertEqual(4, count)

    def test_filter_stage(self) -> None:
        """진료 단계 기준 필터링"""
        self.assertEqual(
            1, MedicalService.objects.filter(stage=MedicalStage.DISCHARGE).count()
        )

    def test_filter_status(self) -> None:
        """진료 단계별 상태 기준 필터링"""
        self.assertEqual(
            1, MedicalService.objects.filter(status=MedicalStageStatus.WAIT).count()
        )

    def test_filter_stage_status(self) -> None:
        """진료 단계 + 상태 기준 필터링"""
        self.assertEqual(
            1,
            MedicalService.objects.filter(
                stage=MedicalStage.EXAMINATION, status=MedicalStageStatus.WAIT
            ).count(),
        )

    def test_valiation_register(self) -> None:
        """접수등록 검증"""
        with self.assertRaises(ValidationError):
            self.last.register = None
            self.last.full_clean()

        with self.assertRaises(ValueError):
            self.last.register = ""

        with self.assertRaises(ValueError):
            self.last.register = 999

    def test_valiation_stage(self) -> None:
        """단게 등록 검증"""

        with self.assertRaises(ValidationError):
            self.last.stage = None
            self.last.full_clean()

        with self.assertRaises(ValidationError):
            self.last.stage = ""
            self.last.full_clean()

        with self.assertRaises(ValidationError):
            self.last.stage = "asdf"
            self.last.full_clean()

    def test_valiation_status(self) -> None:
        """단게 상태 검증"""

        with self.assertRaises(ValidationError):
            self.last.status = None
            self.last.full_clean()

        with self.assertRaises(ValidationError):
            self.last.status = ""
            self.last.full_clean()

        with self.assertRaises(ValidationError):
            self.last.status = "zxcvzxcv"
            self.last.full_clean()

    def test_valiation_creator(self) -> None:
        """등록자 검증"""

        with self.assertRaises(ValidationError):
            self.last.creator = None
            self.last.full_clean()

        with self.assertRaises(ValueError):
            self.last.creator = ""

        with self.assertRaises(ValueError):
            self.last.creator = 19238
