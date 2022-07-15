__all__ = ["PatientSerialiezerTestCase", "PatientApiTestCase"]


from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from iamdt.models import Patient
from iamdt_api.serializers import PatientInfoSerializer


class PatientSerialiezerTestCase(TestCase):
    """환자 시리얼라이즈 테스트케이스"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        # "medical_register.json",
        # "medical_detail.json",
        # "medical_staff.json",
    ]

    def setUp(self) -> None:
        self.patient_obj = Patient.objects.get(id=1)
        self.patient_dict = {"name": "환자1", "companion": 1}

    def test_serializer(self) -> None:
        """환자 오브젝트 직렬화 체크"""
        serializer = PatientInfoSerializer(self.patient_obj)
        self.assertEqual("환자1", serializer.data["name"])

        serializer = PatientInfoSerializer(
            self.patient_obj, data={"name": "환자111"}, partial=True
        )
        serializer.is_valid()
        self.assertEqual("환자111", serializer.validated_data["name"])

    def test_validation_name(self) -> None:
        """이름 validation"""
        # blank
        self.patient_dict["name"] = ""
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

        # null
        self.patient_dict["name"] = None
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

        # missing
        self.patient_dict.pop("name")
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

    def test_validation_companion(self) -> None:
        """보호자 validation"""
        # text
        self.patient_dict["companion"] = "1"
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

        # null
        self.patient_dict["companion"] = None
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

        # user not found
        self.patient_dict["companion"] = 9999
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

        # missing
        self.patient_dict.pop("companion")
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())

    def test_validation_unique(self) -> None:
        """보호자+이름 중복 X"""
        serializer = PatientInfoSerializer(data=self.patient_dict)
        self.assertFalse(serializer.is_valid())


class PatientApiTestCase(APITestCase):
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
        # {"name": "환자1", "companion": 1}
        self.patient = Patient.objects.get(id=1)

        # url_info
        self.urls = {
            "list": "/api/patients",
            "create": "/api/patients",
            "read": "/api/patients/1",
            "update": "/api/patients/1",
            "delete": "/api/patients/1",
        }

        # new patient
        self.new_patient = {"name": "신규환자", "companion": 1}

        # clinet login
        login_user = {"username": "doctor1", "password": "doc12345678"}
        self.client.login(**login_user)

    def test_url(self) -> None:
        """url 예상대로 생성되었는가"""
        self.assertURLEqual(self.urls["list"], reverse("api:patient:list"))
        self.assertURLEqual(self.urls["create"], reverse("api:patient:list"))
        self.assertURLEqual(
            self.urls["read"], reverse("api:patient:detail", kwargs={"id": 1})
        )
        self.assertURLEqual(
            self.urls["update"], reverse("api:patient:detail", kwargs={"id": 1})
        )
        self.assertURLEqual(
            self.urls["delete"], reverse("api:patient:detail", kwargs={"id": 1})
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
            self.urls["list"], data=self.new_patient, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.new_patient["name"])

    def test_api_read(self) -> None:
        """read api (get)"""
        response = self.client.get(self.urls["read"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "환자1")

    def test_api_update(self) -> None:
        """update api (patch)"""
        response = self.client.patch(
            self.urls["update"], data={"name": "이름수정"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_update_fail(self) -> None:
        """update api (patch). phone validation fail"""
        response = self.client.patch(
            self.urls["update"], data={"name": ""}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_delete(self) -> None:
        """delete api (delete)

        테스트 DB에는 ProtectedError가 발생하니 406코드가 와야 한다
        """
        response = self.client.delete(self.urls["delete"])
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
