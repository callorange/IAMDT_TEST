__all__ = ["LoginApiTestCase"]

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class LoginApiTestCase(APITestCase):
    """로그인 기능 테스트"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_service.json",
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
            data={"username": "doctor1", "password": "1234"},
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
        self.client.login(**{"username": "doctor1", "password": "1234"})
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
