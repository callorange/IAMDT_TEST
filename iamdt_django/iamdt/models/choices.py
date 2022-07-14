from django.db import models


class MedicalStage(models.TextChoices):
    """진료 단계"""

    REGISTER = "register", "접수"
    EXAMINATION = "examination", "진료"
    DIAGNOSYS = "diagnosys", "진단"
    TREATMENT = "treatment", "처치"
    COUNSELING = "counseling", "결과 설명/상담"
    PAYMENT = "payment", "수납"
    DISCHARGE = "discharge", "퇴원"


class MedicalStageStatus(models.TextChoices):
    """진료 단계 상태(대기/완료)"""

    WAIT = "wait", "대기"
    COMPLETE = "complete", "완료"
