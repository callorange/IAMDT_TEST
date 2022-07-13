__all__ = ["IAMDTUser"]

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from iamdt_util.validators import phone_validator


class IAMDTUser(AbstractUser):
    """IAMDT 코딩테스트 프로젝트 기본 유저

    고객/환자는 별도 모델로 저장할 예정이므로
    병원 직원 정보만 등록 예정이다.
    """

    class UserType(models.TextChoices):
        """Role 종류"""

        DOCTOR = "doctor", "수의사"
        NURSE = "nurse", "간호사"
        EMPLOYEE = "employee", "직원"
        DEVELOPER = "developer", "개발자"

    class MessengerType(models.TextChoices):
        """직원별 알림용 메신저 프로그램 종류"""

        DEFAULT = "", "없음"
        KAKAOTALK = "kakaotalk", "카카오톡"
        FACEBOOK = "facebook", "페이스북"
        LINE = "line", "라인"
        TELEGRAM = "telegram", "텔레그램"

    role = models.CharField(
        "역할", choices=UserType.choices, default=UserType.EMPLOYEE, max_length=10
    )
    phone = models.CharField(
        "연락처",
        blank=True,
        max_length=13,
        validators=[phone_validator],
        help_text="SMS 수신이 가능한 연락처",
    )
    messenger = models.CharField(
        "메신저",
        choices=MessengerType.choices,
        default=MessengerType.DEFAULT,
        max_length=10,
        help_text="메신저 종류, 없다면 비워둘 것",
    )
    messenger_id = models.CharField("메신저 아이디", blank=True, max_length=100)

    class Meta:
        verbose_name = "유저"
        verbose_name_plural = "유저 리스트"
