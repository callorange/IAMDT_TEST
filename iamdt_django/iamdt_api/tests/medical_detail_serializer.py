__all__ = ["MedicalServiceSerializerTestCase"]

from django.test import TestCase

from iamdt.models.choices import MedicalStage, MedicalStageStatus
from iamdt_api.serializers.medical_detail import MedicalDetailInfoSerializer


class MedicalServiceSerializerTestCase(TestCase):
    """로그인을 위한 시리얼라이저 테스트"""

    def setUp(self) -> None:
        self.data = {
            "register": 1,
            "stage": MedicalStage.REGISTER,
            "status": MedicalStageStatus.WAIT,
            "creator": 2,
            "staffs": [1, 2, 3],
        }

    def test_validation_patient_id(self) -> None:
        """진료접수 지정 테스트"""
        # text
        self.data["register"] = "1"
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["register"] = None
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # register not found
        self.data["register"] = 9999
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # missing
        self.data.pop("register")
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_stage(self) -> None:
        """의료 단계 검증"""
        # text
        self.data["stage"] = "1"
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["stage"] = None
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["stage"] = 9999
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_stage_status(self) -> None:
        """의료 단계 상태 검증"""
        # text
        self.data["stage"] = "1"
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # null
        self.data["stage"] = None
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["stage"] = 9999
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_validation_staffs(self) -> None:
        """스태프 지정"""
        # text
        self.data["staff"] = "1"
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        # number
        self.data["staff"] = 9999
        serializer = MedicalDetailInfoSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
