__all__ = ["medical_staff_change_signal"]

import logging


logger = logging.getLogger(__name__)


def staff_name_role(staff):
    """staff의 이름을 반환한다. 성+이름"""
    return f"{staff.last_name} {staff.first_name} {staff.get_role_display()}"


def medical_staff_noti_message(staffs, service, msg: str):
    for staff in staffs:
        logger.info(f"{staff_name_role(staff)} 님 {service}의 담당자에 {msg} 되셨습니다")


message = {
    "post_add": "등록",
    "post_remove": "제외",
}


def medical_staff_change_signal(info):
    """진료내역 담당자가 바뀔경우 시그널에서 호출할 함수

    m2m_changed signal
    {
        'signal': <django.db.models.signals.ModelSignal object at 0x0000022E82BC2E00>,
        'action': 'pre_add', 'post_add', 'pre_remove', 'post_remove'
        'instance': <MedicalService: 고객1(01011112222) / 환자1 의 진료2번 / 진단(대기)>,
        'reverse': False,
        'model': <class 'iamdt.models.user.User'>,
        'pk_set': {5},
        'using': 'default'
    }
    """
    # 추가/삭제 된 유저
    staffs = info["model"].objects.filter(id__in=list(info["pk_set"]))

    # 등록/제외 구분
    msg = message.get(info["action"], None)

    # pre 일때는 빼고 post_** 일때 호출
    if msg:
        medical_staff_noti_message(staffs, info["instance"], msg)
