__all__ = ["MedicalService", "MedicalStaff", "medical_staff_changed"]

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from iamdt.models import Patient, MedicalRegister
from iamdt.models.choices import MedicalStage, MedicalStageStatus
from iamdt_util.notification import medical_staff_change_signal


class MedicalService(models.Model):
    """진료 내역 모델"""

    patient = models.ForeignKey(
        Patient,
        related_name="services",
        verbose_name="환자",
        on_delete=models.PROTECT,
    )
    register = models.ForeignKey(
        MedicalRegister,
        related_name="details",
        verbose_name="접수번호",
        on_delete=models.PROTECT,
    )

    stage = models.CharField(
        "단계",
        choices=MedicalStage.choices,
        default=MedicalStage.REGISTER,
        max_length=15,
    )
    status = models.CharField(
        "상태",
        choices=MedicalStageStatus.choices,
        default=MedicalStageStatus.WAIT,
        max_length=15,
    )

    creator = models.ForeignKey(
        get_user_model(),
        related_name="create_stage",
        verbose_name="등록자",
        on_delete=models.PROTECT,
        limit_choices_to={"is_staff": True, "is_active": True},
    )
    staff = models.ManyToManyField(
        get_user_model(),
        through="MedicalStaff",
        related_name="schedule",
        verbose_name="담당자",
        through_fields=("detail", "staff"),
    )

    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "진료내역"
        verbose_name_plural = "진료내역 리스트"

    def __str__(self) -> str:
        return (
            f"{self.register} / {self.get_stage_display()}({self.get_status_display()})"
        )


class MedicalStaff(models.Model):
    """
    진료 단계별 담당자
    중개모델로 User와 MedicalDetail를 연결한다.
    Source: MedicalDetail
    Target: User
    """

    detail = models.ForeignKey(
        MedicalService,
        verbose_name="진료단계",
        on_delete=models.CASCADE,
    )
    staff = models.ForeignKey(
        get_user_model(),
        verbose_name="담당자",
        on_delete=models.RESTRICT,
    )

    created_at = models.DateTimeField("등록일", auto_now_add=True)

    class Meta:
        verbose_name = "진료내역별 담당자"
        verbose_name_plural = "진료내역별 담당자 리스트"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.staff}/{self.detail}"


@receiver(m2m_changed, sender=MedicalService.staff.through)
def medical_staff_changed(sender, **kwargs):
    medical_staff_change_signal(kwargs)
