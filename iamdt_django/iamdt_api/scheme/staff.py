"""
스태프 API 문서화 관련 데이터
"""

__all__ = ["staff_api_examples"]

from drf_spectacular.utils import OpenApiExample

_read_example = [
    OpenApiExample(
        name="스태프 정보",
        summary="스태프(병원관계자) 정보 조회",
        description="스태프(병원관계자)의 정보 조회",
        value={
            "id": 2,
            "username": "doctor2",
            "first_name": "name2",
            "last_name": "doc",
            "role": "doctor",
            "role_display": "수의사",
            "phone": "01012345678",
            "messenger": "kakaotalk",
            "messenger_id": "doc2",
            "is_staff": True,
            "is_superuser": False,
        },
        response_only=True,
    )
]
_add_example = [
    OpenApiExample(
        name="스태프 등록",
        summary="스태프(병원관계자) 정보 등록",
        description="스태프(병원관계자)의 정보 등록<br>role을 지정하지 않으면 doctor로 기본 지정됨",
        value={
            "username": "doctor2",
            "password": "123123",
            "first_name": "name2",
            "last_name": "doc",
            "role": "doctor",
            "phone": "01012345678",
            "messenger": "kakaotalk",
            "messenger_id": "doc2",
        },
        request_only=True,
    ),
    OpenApiExample(
        name="스태프 등록 실패",
        summary="스태프(병원관계자) 정보 등록 실패",
        description="스태프(병원관계자)의 정보 등록 실패를 테스트를 위한 예제",
        value={"username": "doctor2"},
        request_only=True,
    ),
]
_mod_example = [
    OpenApiExample(
        name="스태프 수정1",
        summary="스태프(병원관계자) 정보 수정",
        description="role과 messenger의 choices value 선택에 주의",
        value={
            "first_name": "name1",
            "last_name": "doc",
            "role": "doctor",
            "phone": "01012345678",
            "messenger": "kakaotalk",
            "messenger_id": "doc1",
        },
        request_only=True,
    ),
    OpenApiExample(
        name="스태프 수정2",
        summary="스태프(병원관계자) 정보 수정 실패",
        description="스태프(병원관계자)의 정보 수정 실패 예제. 핸드폰 번호는 비워둘 수 없다",
        value={
            "first_name": "name1",
            "last_name": "doc",
            "role": "doctor",
            "phone": "",
            "messenger": "kakaotalk",
            "messenger_id": "doc1",
        },
        request_only=True,
    ),
]

staff_api_examples = {
    "read": _read_example,
    "add": _add_example + _read_example,
    "mod": _mod_example + _read_example,
    "all": _add_example + _mod_example + _read_example,
}
