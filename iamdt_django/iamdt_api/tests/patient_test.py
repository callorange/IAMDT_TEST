__all__ = ["PatientSerialiezerTestCase"]


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
        self.assertEqual("환자111", serializer.validated_data["환자111"])

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
