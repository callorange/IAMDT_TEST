__all__ = ["MedicalRegister"]

from django.db import models

from iamdt.models import Patient


class MedicalRegister(models.Model):
    """진료 접수 모델"""

    patient = models.ForeignKey(
        Patient,
        related_name="registers",
        verbose_name="환자",
        on_delete=models.PROTECT,
    )

    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "진료 접수"
        verbose_name_plural = "진료 접수 리스트"

    def __str__(self) -> str:
        return f"{self.patient} / 진료{self.id}"

    @property
    def current_stage(self) -> str:
        """진료 접수의 현재 상태 반환"""
        return str(self.details.last())
