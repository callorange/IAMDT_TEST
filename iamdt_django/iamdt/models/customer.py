__all__ = ["Customer"]

from django.db import models

from iamdt_util.validators import phone_validator


class Customer(models.Model):
    """고객정보 모델"""

    name = models.CharField("이름", max_length=100)
    phone = models.CharField(
        "연락처",
        max_length=13,
        validators=[phone_validator],
        help_text="SMS 수신이 가능한 연락처",
    )

    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "고객"
        verbose_name_plural = "고객 리스트"
        constraints = [
            models.UniqueConstraint(fields=["name", "phone"], name="customer_unique")
        ]

    def __str__(self) -> str:
        return f"{self.name}({self.phone})"
