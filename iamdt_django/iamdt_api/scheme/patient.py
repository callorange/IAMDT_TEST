"""
환자 API 문서화 관련 데이터
"""

__all__ = ["patient_api_url_param", "patient_api_examples"]

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

# 환자 url path kwargs
patient_api_url_param = OpenApiParameter(
    "id",
    OpenApiTypes.INT,
    OpenApiParameter.PATH,
    description="조회할 환자 고유번호",
    examples=[
        OpenApiExample(name="환자1", value=1),
        OpenApiExample(name="환자2", value=2),
        OpenApiExample(name="환자3", value=3),
    ],
)

# serialzier example
_read_example = [
    OpenApiExample(
        name="환자정보1",
        summary="환자정보 조회",
        description="read_only 필드인 id, created_at, updated_at가 포함 됩니다.",
        value={
            "id": "1",
            "companion": 1,
            "name": "신규환자",
            "created_at": "2022-07-13T10:28:31.680Z",
            "updated_at": "2022-07-13T10:30:21.885Z",
        },
        response_only=True,
    )
]
_add_example = [
    OpenApiExample(
        name="신규환자1",
        summary="환자정보 등록 성공",
        description="보호자 pk가 필요하며 동일 보호자에게 같은 이름의 환자는 등록 불가합니다.",
        value={"companion": 1, "name": "신규환자"},
        request_only=True,
    ),
    OpenApiExample(
        name="신규환자2",
        summary="환자정보 등록 실패(누락)",
        description="보호자 pk 혹은 이름은 모두 필수 값 입니다.",
        value={"name": "신규환자"},
        request_only=True,
    ),
    OpenApiExample(
        name="신규환자3",
        summary="환자정보 등록 실패(중복)",
        description="보호자 pk + 환자이름 은 중복될 수 없습니다.(테스트시 기존 정보를 확인하세요)",
        value={"companion": 1, "name": "환자1"},
        request_only=True,
    ),
]
_mod_example = [
    OpenApiExample(
        name="환자정보수정1",
        summary="환자정보 수정",
        description="환자의 이름을 수정합니다.",
        value={"name": "신규환자"},
        request_only=True,
    ),
    OpenApiExample(
        name="환자정보수정2",
        summary="환자정보 수정(동행인변경)",
        description="동행인을 변경 할 수 있습니다. 할일은 없겠지만요 :)",
        value={"companion": 1, "name": "신규환자"},
        request_only=True,
    ),
    OpenApiExample(
        name="환자정보수정3",
        summary="환자정보 수정결과",
        description="read_only 필드인 id, created_at, updated_at가 포함 됩니다.",
        value={
            "id": "1",
            "companion": 1,
            "name": "신규환자",
            "created_at": "2022-07-13T10:28:31.680Z",
            "updated_at": "2022-07-13T10:30:21.885Z",
        },
        response_only=True,
    ),
]
patient_api_examples = {
    "read": _read_example,
    "add": _add_example + _read_example,
    "mod": _mod_example + _read_example,
    "all": _add_example + _mod_example + _read_example,
}
