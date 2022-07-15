"""
진료내역 API 문서화 관련 데이터
"""

__all__ = ["service_api_url_param", "service_api_examples"]

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

# 진료내역 url path kwargs
service_api_url_param = OpenApiParameter(
    "id",
    OpenApiTypes.INT,
    OpenApiParameter.PATH,
    description="진료 내역 고유번호",
    examples=[
        OpenApiExample(name="1", value=1),
        OpenApiExample(name="2", value=2),
        OpenApiExample(name="3", value=3),
    ],
)

# serialzier example
_read_example = [
    OpenApiExample(
        name="진료내역정보1",
        summary="진료내역정보 조회",
        description="read_only 필드인 id, created_at, updated_at가 포함 됩니다.",
        value={
            "id": 1,
            "patient": 1,
            "register": 1,
            "stage": "register",
            "stage_display": "접수",
            "status": "wait",
            "status_display": "대기",
            "creator": 4,
            "staff": [
                {
                    "id": "4",
                    "username": "employee1",
                    "first_name": "name1",
                    "last_name": "employee",
                    "role_display": "직원",
                }
            ],
            "created_at": "2022-07-13T10:28:31.680Z",
            "updated_at": "2022-07-13T10:30:21.885Z",
        },
        response_only=True,
    )
]
_add_example = [
    OpenApiExample(
        name="진료내역등록1",
        summary="진료내역정보 등록",
        description="환자, 진료단계, 담당스태프 3개 정보만 받습니다. 담당자는 담당자 고유번호 list로 보내져야 합니다",
        value={"patient": 1, "stage": "register", "staff": [4]},
        request_only=True,
    ),
    OpenApiExample(
        name="진료내역등록2",
        summary="진료내역정보 등록 실패(누락)",
        description="환자, 진료단계, 담당스태프 3개 정보는 필수 입니다.",
        value={"stage": "register"},
        request_only=True,
    ),
    OpenApiExample(
        name="진료내역등록3",
        summary="진료내역정보 등록 실패(잘못된 진료단계)",
        description="기존 진료단계에서 진행 할 수 없는 단계로 등록시 오류가 발생 합니다.",
        value={"patient": 1, "stage": "register", "staff": [4]},
        request_only=True,
    ),
]
_mod_example = [
    OpenApiExample(
        name="진료내역수정1",
        summary="진료내역정보 수정(스태프)",
        description="담당 스태프를 변경합니다. 담당스태프 pk의 list를 보내야 합니다.",
        value={"staff": [2, 3, 4]},
        request_only=True,
    ),
    OpenApiExample(
        name="진료내역수정2",
        summary="진료내역정보 수정(상태변경)",
        description="진료내역의 상태를 수정합니다. (다음단계 이행시 자동으로 완료 처리 됩니다. ;ㅁ;)",
        value={"status": "complete"},
        request_only=True,
    ),
    OpenApiExample(
        name="진료내역수정3",
        summary="진료내역 수정(실패)",
        description="진료단계 상태와 담당 스태프는 동시에 수정 할 수 없습니다.",
        value={"status": "complete", "staff": [1, 2, 3]},
        request_only=True,
    ),
    OpenApiExample(
        name="진료내역수정4",
        summary="진료내역정보 수정결과",
        description="read_only 필드인 id, created_at, updated_at가 포함 됩니다.",
        value={
            "id": 1,
            "patient": 1,
            "register": 1,
            "stage": "register",
            "stage_display": "접수",
            "status": "wait",
            "status_display": "대기",
            "creator": 4,
            "staff": [
                {
                    "id": "4",
                    "username": "employee1",
                    "first_name": "name1",
                    "last_name": "employee",
                    "role_display": "직원",
                }
            ],
            "created_at": "2022-07-13T10:28:31.680Z",
            "updated_at": "2022-07-13T10:30:21.885Z",
        },
        response_only=True,
    ),
]
service_api_examples = {
    "read": _read_example,
    "add": _add_example + _read_example,
    "mod": _mod_example + _read_example,
    "all": _add_example + _mod_example + _read_example,
}
