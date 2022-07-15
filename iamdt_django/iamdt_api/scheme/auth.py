"""
인증 API 문서화 관련 데이터
"""

__all__ = ["auth_api_examples"]

from drf_spectacular.utils import OpenApiExample

_read_example = []
_add_example = [
    OpenApiExample(
        name="로그인 요청1",
        summary="로그인 요청 성공",
        description="로그인 요청시 제출 되어야 하는 데이터 입니다.",
        value={"username": "doctor1", "password": "doc12345678"},
        request_only=True,
    ),
    OpenApiExample(
        name="로그인 요청2",
        summary="로그인 요청 실패",
        description="로그인 요청이 실패하는 데이터",
        value={"username": "doctor1"},
        request_only=True,
    ),
]
_mod_example = []

auth_api_examples = {
    "read": _read_example,
    "add": _add_example + _read_example,
    "mod": _mod_example + _read_example,
    "all": _add_example + _mod_example + _read_example,
}
