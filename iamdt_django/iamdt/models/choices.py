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


# 진행 가능한 단계
POSSIBLE_STAGES = {
    # 접수 -> 진료, 퇴원
    MedicalStage.REGISTER: [MedicalStage.EXAMINATION, MedicalStage.DISCHARGE],
    # 진료 -> 진료, 진단, 처치, 상담
    MedicalStage.EXAMINATION: [
        MedicalStage.EXAMINATION,
        MedicalStage.DIAGNOSYS,
        MedicalStage.TREATMENT,
        MedicalStage.COUNSELING,
    ],
    # 진단 -> 진료, 처치, 상담
    MedicalStage.DIAGNOSYS: [
        MedicalStage.EXAMINATION,
        MedicalStage.TREATMENT,
        MedicalStage.COUNSELING,
    ],
    # 처치 -> 진료, 진단, 상담
    MedicalStage.TREATMENT: [
        MedicalStage.EXAMINATION,
        MedicalStage.DIAGNOSYS,
        MedicalStage.COUNSELING,
    ],
    # 상담 -> 접수, 수납, 퇴원
    MedicalStage.COUNSELING: [
        MedicalStage.REGISTER,
        MedicalStage.PAYMENT,
        MedicalStage.DISCHARGE,
    ],
    # 수납 -> 퇴원
    MedicalStage.PAYMENT: [MedicalStage.DISCHARGE],
    # 퇴원 -> -
    MedicalStage.DISCHARGE: [],
}


class MedicalStageStatus(models.TextChoices):
    """진료 단계 상태(대기/완료)"""

    WAIT = "wait", "대기"
    COMPLETE = "complete", "완료"
