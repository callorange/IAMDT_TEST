__all__ = ["Register"]

from django.db import models

from iamdt.models import Patient


class MedicalStage(models.TextChoices):
    """진료 단계"""

    REGISTER = "register", "접수"
    EXAMINATION = "examination", "진료"
    DIAGNOSYS = "diagnosys", "진단"
    TREATMENT = "treatment", "처치"
    COUNSELING = "counseling", "결과 설명/상담"
    PAYMENT = "payment", "수납"
    DISCHARGE = "discharge", "퇴원"


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
