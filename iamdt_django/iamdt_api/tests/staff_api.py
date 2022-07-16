__all__ = ["StaffApiTestCase"]


from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


class StaffApiTestCase(APITestCase):
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
        self.staff = get_user_model().objects.get(id=2)

        self.login_url = reverse("api:auth:login")

        self.staff_list_url = reverse("api:staff:list")
        self.staff_info_url = reverse("api:staff:detail", kwargs={"id": 2})

        self.doc1_data = {"username": "doctor1", "password": "1234"}
        self.new_doc_data = {
            "username": "doctor2",
            "password": "1234",
            "first_name": "name222222",
            "last_name": "doc",
            "role": "doctor",
            "phone": "01012345678",
            "messenger": "kakaotalk",
            "messenger_id": "doc2",
        }
        self.client.login(**self.doc1_data)

    def test_url_reverse(self) -> None:
        """URL reverse로 django에 url이 등록되었는지 확인"""
        self.assertURLEqual("/api/staffs", self.staff_list_url)
        self.assertURLEqual("/api/staffs/2", self.staff_info_url)

    def test_url_options(self) -> None:
        """URL에 options 요청이 가는지 확인"""
        response = self.client.options(self.staff_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.options(self.staff_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_options_no_auth(self) -> None:
        """URL에 인증없이 options 요청"""
        client = APIClient()
        response = client.options(self.staff_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.options(self.staff_info_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_list(self) -> None:
        """staff list 확인"""
        response = self.client.get(self.staff_list_url, data={"page_size": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_create(self) -> None:
        """staff 등록"""
        response = self.client.post(
            self.staff_list_url, data=self.new_doc_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.new_doc_data["username"])

    def test_staff_info(self) -> None:
        """staff 정보"""
        response = self.client.get(self.staff_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.doc1_data["username"])

    def test_staff_patch(self) -> None:
        """staff 정보 업데이트"""
        response = self.client.patch(
            self.staff_info_url, data={"phone": ""}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            self.staff_info_url, data={"phone": "01099999999"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_put(self) -> None:
        """staff 정보 업데이트"""
        # 성공
        response = self.client.patch(
            self.staff_info_url,
            data={
                "username": "doctor1",
                "first_name": "name222222",
                "last_name": "doc",
                "role": "doctor",
                "phone": "01012345678",
                "messenger": "kakaotalk",
                "messenger_id": "doc2",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "name222222")

        # 변경권한 없음 403
        response = self.client.patch(
            reverse("api:staff:detail", kwargs={"id": 3}),
            data={
                "first_name": "name2",
                "last_name": "doc",
                "role": "doctor",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
