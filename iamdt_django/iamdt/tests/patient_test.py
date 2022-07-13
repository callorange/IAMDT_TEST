__all__ = ["PatientModelTestCase"]

from django.test import TestCase
from django.core.exceptions import ValidationError

from iamdt.models import Customer, Patient
from iamdt.tests.customer_test import test_customer_info

test_patient_info = [
    {"name": "환자이름", "age": 11},
    {"name": "환자이름", "age": 5},
    {"name": "름이자환", "age": 5},
    {"name": "환자이름", "age": 8},
]


class PatientModelTestCase(TestCase):
    """
    환자 모델 테스트
    """

    def setUp(self) -> None:
        """고객을 외래키로 참조하므로 고객정보도 필요하다."""
        # 고객/환자 정보 생성
        for customer_info, patient_info in zip(test_customer_info, test_patient_info):
            customer = Customer.objects.create(**customer_info)
            Patient.objects.create(companion=customer, **patient_info)

    def test_info(self) -> None:
        """생성된 정보 확인"""
        customer_info = test_customer_info[0]
        patient_info = test_patient_info[0]
        customer = Customer.objects.get(
            name=customer_info["name"], phone=customer_info["phone"]
        )
        patient = Patient.objects.get(companion=customer, name=patient_info["name"])

        # 이름 확인
        self.assertEqual(patient.name, patient_info["name"])

        # 보호자 이름 확인
        self.assertEqual(patient.companion.name, customer_info["name"])

    def test_filter(self) -> None:
        """환자 모델 검색 기능 테스트"""
        # 등록된 환자는 4명
        self.assertEqual(4, Patient.objects.all().count())

        # 나이가 5살인 환자는 2명
        self.assertEqual(2, Patient.objects.filter(age=5).count())

        # 이름이 같은 환자는 3명
        self.assertEqual(3, Patient.objects.filter(name="환자이름").count())

    def test_validation(self) -> None:
        """환자 모델 validation 테스트"""
        patient = Patient.objects.first()

        # 이름은 비어있으면 안된다
        patient.refresh_from_db()
        patient.name = ""
        with self.assertRaises(ValidationError):
            patient.full_clean()

        # 나이는 0살 이상이어야 한다.
        patient.refresh_from_db()
        patient.age = -1
        with self.assertRaises(ValidationError):
            patient.full_clean()
