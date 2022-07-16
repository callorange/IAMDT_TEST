__all__ = ["LoginSerializerTestCase"]

from django.test import TestCase

from iamdt_api.serializers.auth import LoginSerializer


class LoginSerializerTestCase(TestCase):
    """로그인을 위한 시리얼라이저 테스트"""

    def test_serializer_validation_username(self) -> None:
        """계정명 검증 테스트"""
        serializer = LoginSerializer(data={"password": "doctor1"})
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_password(self) -> None:
        """비밀번호가 검증 테스트"""
        serializer = LoginSerializer(data={"username": "doctor1"})
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation(self) -> None:
        """데이터가 제대로 지정됬을때"""
        serializer = LoginSerializer(data={"username": "doctor1", "password": "1234"})
        self.assertTrue(serializer.is_valid())
