__all__ = ["CustomerSerialiezerTestCase", "StaffApiTestCase"]


from django.test import TestCase
from rest_framework import status

from iamdt.models import Customer
from iamdt_api.serializers import CustomerInfoSerializer
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


class CustomerSerialiezerTestCase(TestCase):
    """
    고객 시리얼라이저 테스트
    """

    fixtures = ["user.json", "customer.json"]

    def setUp(self) -> None:
        self.customer_obj = Customer.objects.get(id=1)
        self.customer_dict = {"name": "고객1", "phone": "01011112222"}

    def test_serializer(self) -> None:
        """고객 객체가 주어졌을때"""
        serializer = CustomerInfoSerializer(self.customer_obj)
        self.assertEqual("고객1", serializer.data["name"])

        serializer = CustomerInfoSerializer(
            self.customer_obj, data={"phone": "01099999999"}, partial=True
        )
        serializer.is_valid()
        self.assertEqual("01099999999", serializer.validated_data["phone"])

    def test_validation_name(self) -> None:
        """이름 validation"""
        # blank
        self.customer_dict["name"] = ""
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # null
        self.customer_dict["name"] = None
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # missing
        self.customer_dict.pop("name")
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

    def test_validation_phone(self) -> None:
        """연락처 validation"""
        # regex
        self.customer_dict["phone"] = "11122223333"
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # blank
        self.customer_dict["phone"] = ""
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # null
        self.customer_dict["phone"] = None
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

        # missing
        self.customer_dict.pop("phone")
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())

    def test_validation_unique(self) -> None:
        """이름+연락처 복합키를 사용하므로 중복 X"""
        serializer = CustomerInfoSerializer(data=self.customer_dict)
        self.assertFalse(serializer.is_valid())


class StaffApiTestCase(APITestCase):
    """고객정보 api 테스트"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_detail.json",
        "medical_staff.json",
    ]

    def setUp(self) -> None:
        # {"name": "고객1", "phone": "01011112222"}
        self.customer = Customer.objects.get(id=1)

        # url_info
        self.urls = {
            "list": "/api/customers",
            "create": "/api/customers",
            "read": "/api/customers/1",
            "update": "/api/customers/1",
            "delete": "/api/customers/1",
        }

        # new customer
        self.new_customer = {"name": "신규고객", "phone": "01098765432"}

        # clinet login
        login_user = {"username": "doctor1", "password": "doc12345678"}
        self.client.login(**login_user)

    def test_url(self) -> None:
        """url 예상대로 생성되었는가"""
        self.assertURLEqual(self.urls["list"], reverse("api:customer:list"))
        self.assertURLEqual(self.urls["create"], reverse("api:customer:list"))
        self.assertURLEqual(
            self.urls["read"], reverse("api:customer:detail", kwargs={"id": 1})
        )
        self.assertURLEqual(
            self.urls["update"], reverse("api:customer:detail", kwargs={"id": 1})
        )
        self.assertURLEqual(
            self.urls["delete"], reverse("api:customer:detail", kwargs={"id": 1})
        )

    def test_url_option(self) -> None:
        """url access"""
        response = self.client.options(self.urls["list"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.options(self.urls["read"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_option_no_auth(self) -> None:
        """url에 인증 없이 option 요청"""
        client = APIClient()

        response = client.options(self.urls["list"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.options(self.urls["read"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_list(self) -> None:
        """list api(get)"""
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_create(self) -> None:
        """create api (post)"""
        response = self.client.post(
            self.urls["list"], data=self.new_customer, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.new_customer["name"])

    def test_api_read(self) -> None:
        """read api (get)"""
        response = self.client.get(self.urls["read"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "고객1")

    def test_api_update(self) -> None:
        """update api (patch)"""
        response = self.client.patch(
            self.urls["update"], data={"phone": "01099999999"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_update_fail(self) -> None:
        """update api (patch). phone validation fail"""
        response = self.client.patch(
            self.urls["update"], data={"phone": ""}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_delete(self) -> None:
        """delete api (delete)

        테스트 DB에는 ProtectedError가 발생하니 406코드가 와야 한다
        """
        response = self.client.delete(self.urls["delete"])
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
