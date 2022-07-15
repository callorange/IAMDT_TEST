"""
스태프 API 문서화 관련 데이터
"""

__all__ = ["STAFF_API_SEARCH_QUERY", "STAFF_API_EXAMPLES"]

from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

# 스태프 검색 쿼리
STAFF_API_SEARCH_QUERY = [
    OpenApiParameter(
        "username",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        description="스태프 계정명 검색",
    ),
    OpenApiParameter(
        "role",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        enum=get_user_model().UserType,
        description="지정된 스태프 역할로 검색",
    ),
    OpenApiParameter(
        "phone",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        enum=get_user_model().UserType,
        description="전화번호로 검색",
    ),
    OpenApiParameter(
        "o",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        enum=["username", "role", "created_at", "-username", "-role", "-created_at"],
        description="정렬조건.",
    ),
]

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

STAFF_API_EXAMPLES = {
    "read": _read_example,
    "add": _add_example + _read_example,
    "mod": _mod_example + _read_example,
    "all": _add_example + _mod_example + _read_example,
}
