__all__ = ["MedicalRegisterSerializerTestCase"]


from django.test import TestCase

from iamdt.models import MedicalRegister
from iamdt_api.serializers.medical_register import MedicalRegisterInfoSerializer


class MedicalRegisterSerializerTestCase(TestCase):
    """진료접수번호 시리얼라이저 테스트

    진료내역 단위를 구분을 하고 응답시 그룹핑을 위한 DB라 크게 신경쓸건 없다.
    응답내용만 제대로 오는지 확인한다
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
        self.register = MedicalRegister.objects.first()

    def test_nested_service(self) -> None:
        serializer = MedicalRegisterInfoSerializer(self.register)
        data = serializer.data

        self.assertEqual(data["id"], 1)
        self.assertEqual(len(data["details"]), 4)  # 접수번호1의 내역은 총4개
