__all__ = ["MedicalServiceSerializerTestCase"]

from django.test import TestCase

from iamdt.models.choices import MedicalStage, MedicalStageStatus
from iamdt_api.serializers.medical_service import MedicalServiceInfoSerializer


class MedicalServiceSerializerTestCase(TestCase):
    """진료내역 시리얼라이저 테스트

    접수번호는 등록시 자동으로 할당 될것이니 테스트 하지 않는다
    """

    def setUp(self) -> None:
        self.data = {
            "register": 1,
            "stage": MedicalStage.REGISTER,
            "status": MedicalStageStatus.WAIT,
            "creator": 2,
            "staffs": [1, 2, 3],
        }

    def test_validation_patient_id(self) -> None:
        """환자번호 지정 테스트"""
        # text
        self.data["patient"] = "1"
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["patient"] = None
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # register not found
        self.data["patient"] = 9999
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # missing
        self.data.pop("patient")
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_stage(self) -> None:
        """의료 단계 검증"""
        # text
        self.data["stage"] = "1"
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["stage"] = None
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["stage"] = 9999
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_stage_status(self) -> None:
        """의료 단계 상태 검증"""
        # text
        self.data["stage"] = "1"
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["stage"] = None
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["stage"] = 9999
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_staffs(self) -> None:
        """스태프 지정"""
        # text
        self.data["staff"] = "1"
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["staff"] = 9999
        serializer = MedicalServiceInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
