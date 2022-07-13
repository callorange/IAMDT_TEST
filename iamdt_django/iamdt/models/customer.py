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
    email = models.EmailField("이메일주소", blank=True)

    class Meta:
        verbose_name = "고객"
        verbose_name_plural = "고객 리스트"
        constraints = [
            models.UniqueConstraint(fields=["name", "phone"], name="customer_unique")
        ]

    def __str__(self):
        return f"{self.name}({self.phone})"
