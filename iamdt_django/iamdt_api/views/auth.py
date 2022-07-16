"""
API 인증 관련 View
"""

__all__ = ["Login", "Logout"]

from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from iamdt_api.scheme.auth import AUTH_API_EXAMPLES
from iamdt_api.serializers import LoginSerializer, StaffInfoSerializer


class Login(APIView):
    """로그인 API"""

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=["인증"],
        summary="로그인 요청 처리",
        request=LoginSerializer,
        responses={
            200: StaffInfoSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        examples=AUTH_API_EXAMPLES["add"],
    )
    def post(self, request, *args, **kwargs):
        """테스트용이어서 Session을 이용하도록 처리함"""
        self._authenticate(request, self._validate(request))
        return Response(
            StaffInfoSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    def _validate(self, request) -> LoginSerializer:
        """제출 데이터 유효성 검증"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _authenticate(self, request, serializer) -> None:
        """인증 처리"""
        validated_data = serializer.validated_data
        user = authenticate(
            request,
            username=validated_data["username"],
            password=validated_data["password"],
        )
        if user is not None:
            login(request, user)
        else:
            raise exceptions.AuthenticationFailed("ID 혹은 비밀번호가 잘못되었습니다.")


class Logout(generics.GenericAPIView):
    """로그아웃 API"""

    @extend_schema(
        tags=["인증"],
        summary="로그아웃 요청 처리",
        responses={
            204: None,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
    )
    def get(self, request, *args, **kwargs):
        """로그아웃 처리를 한다.
        정상처리시 응답 본문은 없다."""
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
