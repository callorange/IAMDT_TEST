__all__ = ["Patient"]

from django.db import models

from iamdt.models import Customer


class Patient(models.Model):
    """환자 정보 모델"""

    companion = models.ForeignKey(
        Customer,
        related_name="patients",
        verbose_name="동행인",
        on_delete=models.PROTECT,
        help_text="병원 입장에서는 고객이지만 환자 입장에서는 동행인입니다.",
    )

    name = models.CharField("이름", max_length=100)

    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "환자"
        verbose_name_plural = "환자 리스트"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.companion}-{self.name}"
