"""
Patient Api View
"""

__all__ = ["PatientList", "PatientDetail"]

from django.db.models import ProtectedError
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from rest_framework import generics, permissions, exceptions

from iamdt.models import Patient
from iamdt_api.scheme import PAGINATION_QUERY_SCHEME
from iamdt_api.serializers import PatientInfoSerializer
from iamdt_api.scheme.patient import patient_api_examples, patient_api_url_param


class PatientList(generics.ListCreateAPIView):
    """환자 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = Patient.objects.order_by("-id")
    serializer_class = PatientInfoSerializer

    @extend_schema(
        tags=["환자"],
        summary="환자 검색",
        description="환자 리스트를 검색합니다",
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
        examples=patient_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["환자"],
        summary="환자 등록",
        description="신규 환자 등록합니다. 등록시 보호자가 지정되어야 합니다",
        request=PatientInfoSerializer,
        responses={
            200: PatientInfoSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        examples=patient_api_examples["add"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser]
    queryset = Patient.objects.all()
    serializer_class = PatientInfoSerializer

    lookup_url_kwarg = "id"

    @extend_schema(
        parameters=[patient_api_url_param],
        tags=["환자"],
        summary="환자 조회",
        description="환자의 정보를 조회합니다",
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=patient_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        parameters=[patient_api_url_param],
        tags=["환자"],
        summary="환자 수정(put)",
        description="정보를 수정합니다. 동행인 정보에 주의하세요",
        request=PatientInfoSerializer,
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=patient_api_examples["mod"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        parameters=[patient_api_url_param],
        tags=["환자"],
        summary="환자 수정(patch)",
        description="정보를 수정합니다. 동행인 정보에 주의하세요",
        request=PatientInfoSerializer,
        responses={
            200: PatientInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=patient_api_examples["mod"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        parameters=[patient_api_url_param],
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
    )
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            raise exceptions.NotAcceptable(
                detail="Unable to delete for data protection", code="protected_data"
            )
        except Exception as e:
            raise e
