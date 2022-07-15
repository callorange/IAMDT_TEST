__all__ = ["StaffSerializerTestCase"]


from django.contrib.auth import get_user_model
from django.test import TestCase

from iamdt_api.serializers import StaffInfoSerializer


class StaffSerializerTestCase(TestCase):
    """유저 시리얼라이저 테스트"""

    fixtures = ["user.json"]

    def setUp(self) -> None:
        self.staff = get_user_model().objects.get(id=2)

    def test_serializer_validation_user(self) -> None:
        """유저 객체가 지정됬을때"""
        serializer = StaffInfoSerializer(self.staff)
        self.assertEqual("doctor1", serializer.data["username"])

    def test_serializer_data(self) -> None:
        """데이터가 개별 지정됫을때"""
        serializer = StaffInfoSerializer(
            data={
                "username": "doctor1",
                "role": "doctor",
                "phone": "01012345678",
                "messenger": "kakaotalk",
                "messenger_id": "doc1",
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_serializer_false_data(self) -> None:
        """데이터가 개별 지정됫을때"""
        serializer = StaffInfoSerializer(
            data={
                "username": "doctor1",
                "role": "doctor",
                "messenger": "kakaotalk",
                "messenger_id": "doc1",
            }
        )
        self.assertFalse(serializer.is_valid())
