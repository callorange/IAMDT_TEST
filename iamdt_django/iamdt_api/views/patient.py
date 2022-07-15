"""
Patient Api View
"""

__all__ = ["PatientList", "PatientDetail"]

from django.db.models import ProtectedError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import generics, permissions, exceptions

from iamdt.models import Patient
from iamdt_api.scheme import PAGINATION_QUERY_SCHEME
from iamdt_api.serializers import PatientInfoSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["환자"],
        summary="환자 검색",
        description="환자 리스트를 검색합니다",
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
    ),
    post=extend_schema(
        tags=["환자"],
        summary="환자 등록",
        description="신규 환자 등록합니다. 등록시 보호자가 지정되어야 합니다",
        request=PatientInfoSerializer,
        responses={
            200: PatientInfoSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
    ),
)
class PatientList(generics.ListCreateAPIView):
    """환자 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = Patient.objects.order_by("-id")
    serializer_class = PatientInfoSerializer


# 환자 url path kwargs
url_kwargs = OpenApiParameter(
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


@extend_schema_view(
    get=extend_schema(
        parameters=[url_kwargs],
        tags=["환자"],
        summary="환자 조회",
        description="환자의 정보를 조회합니다",
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
    ),
    put=extend_schema(
        parameters=[url_kwargs],
        tags=["환자"],
        summary="환자 수정(put)",
        description="정보를 수정합니다. 동행인 정보에 주의하세요",
        request=PatientInfoSerializer,
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
    ),
    patch=extend_schema(
        parameters=[url_kwargs],
        tags=["환자"],
        summary="환자 수정(patch)",
        description="정보를 수정합니다. 동행인 정보에 주의하세요",
        request=PatientInfoSerializer,
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
    ),
    delete=extend_schema(
        parameters=[url_kwargs],
        tags=["환자"],
        summary="환자 삭제",
        description="지정된 환자 정보룰 삭제합니다.(해당 환자의 접수내역등이 있다면 오류가 발생합니다.)",
        request=PatientInfoSerializer,
        responses={
            200: None,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
            406: OpenApiResponse(description="데이터 보호를 위해 삭제 불가"),
        },
    ),
)
class PatientDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser]
    queryset = Patient.objects.all()
    serializer_class = PatientInfoSerializer

    lookup_url_kwarg = "id"

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except ProtectedError as e:
            raise exceptions.NotAcceptable(
                detail="Unable to delete for data protection", code="protected_data"
            )
        except Exception as e:
            raise e
