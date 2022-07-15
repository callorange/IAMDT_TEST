__all__ = ["MedicalStaffModelTestCase"]

from django.contrib.auth import get_user_model
from django.db.models import Max, Subquery
from django.test import TestCase

from iamdt.models import MedicalService
from iamdt.models.choices import MedicalStageStatus


class MedicalStaffModelTestCase(TestCase):
    """진료 담당자 모델 테스트"""

    fixtures = [
        "user.json",
        "customer.json",
        "patient.json",
        "medical_register.json",
        "medical_service.json",
        "medical_staff.json",
    ]

    def setUp(self) -> None:
        self.details = MedicalService.objects.filter(
            id__in=Subquery(
                MedicalService.objects.values("patient__id")
                .annotate(max_id=Max("id"))
                .values("max_id")
            ),
        )

        self.user_model = get_user_model()
        self.doctor1 = get_user_model().objects.get(id=2)
        self.employee1 = get_user_model().objects.get(id=4)

    def test_filter_staff_doctor(self) -> None:
        """스태프(의사) 기준 필터링"""
        self.assertEqual(
            1,
            self.doctor1.schedule.filter(status=MedicalStageStatus.WAIT)
            .filter(id__in=Subquery(self.details.values("id")))
            .count(),
        )

    def test_filter_staff_employee(self) -> None:
        """스태프(직원) 기준 필터링"""
        self.assertEqual(
            0,
            self.employee1.schedule.filter(status=MedicalStageStatus.WAIT)
            .filter(id__in=Subquery(self.details.values("id")))
            .count(),
        )

    def test_filter_detail(self) -> None:
        """진료단계에서 스태프로 필터링"""
        self.assertEqual(
            1,
            self.details.filter(staff__role=self.user_model.UserType.DOCTOR).count(),
        )
