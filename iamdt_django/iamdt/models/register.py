__all__ = ["Register"]

from django.db import models

from iamdt.models import Patient
from iamdt.models.choices import MedicalStage


class Register(models.Model):
    """진료 접수 모델"""

    patient = models.ForeignKey(
        Patient,
        related_name="registers",
        verbose_name="환자",
        on_delete=models.PROTECT,
    )

    stage = models.CharField(
        "현재단계",
        choices=MedicalStage.choices,
        default=MedicalStage.REGISTER,
        max_length=15,
    )

    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "진료 접수"
        verbose_name_plural = "진료 접수 리스트"

    def __str__(self) -> str:
        return f"{self.patient.name} - {self.get_stage_display()}"
