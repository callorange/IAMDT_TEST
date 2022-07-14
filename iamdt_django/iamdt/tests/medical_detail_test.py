__all__ = ["MedicalStageStatusChoicesTestCase", "MedicalDetailModelTestCase"]

from django.core.exceptions import ValidationError
from django.test import TestCase

from iamdt.models import Register, Patient
from iamdt.models.choices import MedicalStageStatus, MedicalStage
from iamdt.models.medical_detail import MedicalDetail


class MedicalStageStatusChoicesTestCase(TestCase):
    """각 진료 단계별 대기/완료 여부 choices 테스트"""

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
        "register.json",
        "medical_detail.json",
    ]

    def setUp(self) -> None:
        self.last = MedicalDetail.objects.last()

    def test_filter_register(self) -> None:
        """접수등록 기준 필터링"""
        register = Register.objects.first()
        self.assertEqual(4, MedicalDetail.objects.filter(register=register).count())

    def test_filter_stage(self) -> None:
        """진료 단계 기준 필터링"""
        self.assertEqual(
            1, MedicalDetail.objects.filter(stage=MedicalStage.DISCHARGE).count()
        )

    def test_filter_status(self) -> None:
        """진료 단계별 상태 기준 필터링"""
        self.assertEqual(
            1, MedicalDetail.objects.filter(status=MedicalStageStatus.COMPLETE).count()
        )

    def test_filter_stage_status(self) -> None:
        """진료 단계 + 상태 기준 필터링"""
        self.assertEqual(
            1,
            MedicalDetail.objects.filter(
                stage=MedicalStage.EXAMINATION, status=MedicalStageStatus.WAIT
            ).count(),
        )

    def test_filter_patient(self) -> None:
        """환자 진료 내역 필터링"""
        paitent = Patient.objects.get(id=1)
        count = MedicalDetail.objects.filter(register__in=paitent.registers).count()
        self.assertEqual(5, count)

    def test_valiation_register(self) -> None:
        """접수등록 검증(외래키는 엉뚱한게 오면 ValueError)"""
        with self.assertRaises(ValueError):
            self.last = None

        with self.assertRaises(ValueError):
            self.last = ""

        with self.assertRaises(ValueError):
            self.last = 999

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

        with self.assertRaises(ValueError):
            self.last.creator = None
            self.last.full_clean()

        with self.assertRaises(ValueError):
            self.last.creator = ""
            self.last.full_clean()

        with self.assertRaises(ValueError):
            self.last.creator = 19238
            self.last.full_clean()
