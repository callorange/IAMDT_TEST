"""
고객 API 문서화 관련 데이터
"""

__all__ = [
    "CUSTOMER_API_URL_PARAM",
    "CUSTOMER_API_SEARCH_QUERY",
    "CUSTOMER_API_EXAMPLES",
]

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

# 고객 검색 url path kwargs
CUSTOMER_API_URL_PARAM = [
    OpenApiParameter(
        "id",
        OpenApiTypes.INT,
        OpenApiParameter.PATH,
        description="조회할 고객의 고유번호",
        examples=[
            OpenApiExample(name="고객1", value=1),
            OpenApiExample(name="고객2", value=2),
            OpenApiExample(name="고객3", value=3),
        ],
    )
]

# 고객 검색 쿼리 파라미터
CUSTOMER_API_SEARCH_QUERY = [
    OpenApiParameter(
        "name",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        description="이름 검색",
    ),
    OpenApiParameter(
        "phone",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        description="전화번호로 검색",
    ),
    OpenApiParameter(
        "o",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        enum=["name", "phone", "created_at", "-name", "-phone", "-created_at"],
        description="정렬조건.",
    ),
]

# serialzier example
_read_example = [
    OpenApiExample(
        name="고객 정보 조회",
        summary="고객 정보 조회",
        description="고객정보 조회시에는 read_only 필드인 id, created_at, updated_at이 포함된다",
        value={
            "id": "1",
            "name": "고객1",
            "phone": "01022223333",
            "created_at": "2022-07-13T10:28:31.680Z",
            "updated_at": "2022-07-13T10:30:21.885Z",
        },
        response_only=True,
    )
]
_add_example = [
    OpenApiExample(
        name="고객 추가1",
        summary="고객정보 신규 등록",
        description="고객정보를 추가한다. 이름+연락처 결과는 중복될 수 없다.",
        value={"name": "customer1", "phone": "01022223333"},
        request_only=True,
    ),
    OpenApiExample(
        name="고객 추가2",
        summary="고객정보 신규 등록 실패",
        description="이름과 연락처는 모두 필수 값이며, 연락처는 핸드폰 형식에 맞춰 입력되어야 한다.",
        value={"name": "customer1", "phone": "11122223333"},
        request_only=True,
        status_codes=["400"],
    ),
]
_mod_example = [
    OpenApiExample(
        name="고객 수정",
        summary="고객정보 수정",
        description="고객정보를 수정한다 이름+연락처 결과는 중복될 수 없다.",
        value={"name": "customer1", "phone": "01022223333"},
        request_only=True,
    )
]
CUSTOMER_API_EXAMPLES = {
    "read": _read_example,
    "add": _add_example + _read_example,
    "mod": _mod_example + _read_example,
    "all": _add_example + _mod_example + _read_example,
}
