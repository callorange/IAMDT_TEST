__all__ = ["LoginSerializerTestCase", "LoginApiTestCase"]

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

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
        serializer = LoginSerializer(
            data={"username": "doctor1", "password": "doc12345678"}
        )
        self.assertTrue(serializer.is_valid())


class LoginApiTestCase(APITestCase):
    """로그인 기능 테스트"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_detail.json",
        "medical_staff.json",
    ]

    def setUp(self) -> None:
        self.login_url = reverse("api:auth:login")
        self.logout_url = reverse("api:auth:logout")

    def test_login_url_check(self) -> None:
        """로그인 URL이 예정대로인지"""
        self.assertURLEqual("/api/auth/login", self.login_url)

    def test_login_url_head(self) -> None:
        """로그인 URL에 접속이 가능한지"""
        response = self.client.options(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_url(self) -> None:
        """로그인 URL로 로그인이 가능한지"""
        response = self.client.post(
            self.login_url,
            data={"username": "doctor1", "password": "doc12345678"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_url_check(self) -> None:
        """로그아웃 URL이 예정대로인지"""
        self.assertURLEqual("/api/auth/logout", self.logout_url)

    def test_logout_url_head(self) -> None:
        """로그아웃 URL에 접속이 가능한지"""
        response = self.client.options(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # 인증안됨

    def test_logout_url(self) -> None:
        """로그아웃 URL로 로그아웃 되는지"""
        # 로그인 처리를 먼저 한다.
        self.client.login(**{"username": "doctor1", "password": "doc12345678"})
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
