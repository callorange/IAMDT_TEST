__all__ = ["MedicalDetail"]

from django.contrib.auth import get_user_model
from django.db import models

from iamdt.models import Register
from iamdt.models.choices import MedicalStage, MedicalStageStatus


class MedicalDetail(models.Model):
    """진료 내역 모델"""

    register = models.ForeignKey(
        Register,
        related_name="details",
        verbose_name="진료접수",
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
        related_name="details",
        verbose_name="등록자",
        on_delete=models.PROTECT,
        limit_choices_to={"is_staff": True, "is_active": True},
    )

    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "진료 내역"
        verbose_name_plural = "진료 내역"

    def __str__(self) -> str:
        return f"{self.get_stage_display()} - {self.get_status_display()}"
