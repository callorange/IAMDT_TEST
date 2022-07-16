__all__ = ["MedicalServiceInfoSerializerTestCase"]

from django.test import TestCase

from iamdt.models.choices import MedicalStage, MedicalStageStatus
from iamdt_api.serializers.medical_service import (
    MedicalServiceInfoSerializer,
    MedicalServiceAddSerializer,
)


class MedicalServiceAddSerializerTestCase(TestCase):
    """진료내역 등록용 시리얼라이저 테스트"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_service.json",
        "medical_staff.json",
    ]

    def setUp(self) -> None:
        self.data = {"patient": 1, "stage": MedicalStage.DIAGNOSYS, "staff": [2]}

    def test_validate(self) -> None:
        """정상데이터"""
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_validate_patient(self) -> None:
        """유효성 검증"""
        # text
        self.data["patient"] = "a"
        serializer = MedicalServiceAddSerializer(data=self.data)
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())

        # null
        self.data["patient"] = None
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["patient"] = 9999
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # missing
        self.data.pop("patient")
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validate_staff(self) -> None:
        """유효성 검증"""
        # text
        self.data["staff"] = "1"
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["staff"] = None
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["staff"] = 9999
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # int
        self.data["staff"] = 1
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # text in list
        self.data["staff"] = [1, 2, "a"]
        serializer = MedicalServiceAddSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())


class MedicalServiceInfoSerializerTestCase(TestCase):
    """진료내역 시리얼라이저 테스트

    접수번호는 등록시 자동으로 할당 될것이니 테스트 하지 않는다
    """

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_service.json",
        "medical_staff.json",
    ]

    def setUp(self) -> None:
        self.data = {
            "patient": 1,
            "register": 1,
            "stage": MedicalStage.REGISTER,
            "status": MedicalStageStatus.WAIT,
            "creator": 2,
            "staff": [1, 2, 3],
        }

    def test_validation_stage_status(self) -> None:
        """의료 단계 상태 검증"""
        # text
        self.data["status"] = "1"
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["status"] = None
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["status"] = 9999
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_staffs(self) -> None:
        """스태프 지정"""
        # text
        self.data["staff"] = "1"
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["staff"] = None
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["staff"] = 9999
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # int
        self.data["staff"] = 1
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # text in list
        self.data["staff"] = [1, 2, "a"]
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
