"""
Django Spectacular SCHEME 관련 설정 파일을 모아두기 위한 모듈
"""


__all__ = ["PAGINATION_QUERY_SCHEME"]

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample

PAGINATION_QUERY_SCHEME = [
    OpenApiParameter(
        "page",
        OpenApiTypes.INT,
        OpenApiParameter.QUERY,
        description="조회할 페이지",
        examples=[
            OpenApiExample(name="1페이지", value=1),
            OpenApiExample(name="2페이지", value=2),
            OpenApiExample(name="3페이지", value=3),
        ],
    ),
    OpenApiParameter(
        "page_size",
        OpenApiTypes.INT,
        OpenApiParameter.QUERY,
        description="한페이지당 레코드 최대 갯수",
        examples=[
            OpenApiExample(name="최대 1개", value=1),
            OpenApiExample(name="최대 3개", value=3),
            OpenApiExample(name="최대 5개", value=5),
        ],
    ),
]
