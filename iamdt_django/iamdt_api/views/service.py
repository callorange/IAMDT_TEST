"""
MedicalService Api View
"""

__all__ = ["MedicalServiceList", "MedicalServiceDetail"]

from django.db.models import ProtectedError
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, permissions, exceptions

from iamdt.models import MedicalService, MedicalRegister
from iamdt.models.choices import MedicalStageStatus
from iamdt_api.scheme import PAGINATION_QUERY_SCHEME
from iamdt_api.scheme.medical_service import service_api_examples, service_api_url_param
from iamdt_api.serializers.medical_register import MedicalRegisterInfoSerializer
from iamdt_api.serializers.medical_service import (
    MedicalServiceInfoSerializer,
    MedicalServiceAddSerializer,
)


class MedicalServiceList(generics.ListCreateAPIView):
    """진료내역 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = MedicalRegister.objects.order_by("-id")
    serializer_class = MedicalRegisterInfoSerializer

    def get_queryset(self):
        if self.request.method == "POST":
            return MedicalService.objects.order_by("-id")
        return super().get_queryset()

    def get_serializer_class(self):
        """요청 메소드에 따라 시리얼라이저 반환"""
        if self.request.method == "POST":
            return MedicalServiceAddSerializer
        return super().get_serializer_class()

    @extend_schema(
        tags=["진료내역"],
        summary="진료내역 검색",
        description="진료내역 리스트를 검색합니다",
        responses={
            200: MedicalServiceInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
        examples=service_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["진료내역"],
        summary="진료내역 등록",
        description="진료내역을 등록합니다. 등록시 환자/진료단계/담당스태프에 유의하세요",
        request=MedicalServiceAddSerializer,
        responses={
            200: MedicalServiceInfoSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        examples=service_api_examples["add"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """진료내역 등록"""
        obj = serializer.save(creator=self.request.user)  # 등록자는 현재 유저


class MedicalServiceDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser]
    queryset = MedicalService.objects.all()
    serializer_class = MedicalServiceInfoSerializer

    lookup_url_kwarg = "id"

    @extend_schema(
        parameters=[service_api_url_param],
        tags=["진료내역"],
        summary="진료내역 조회",
        description="진료내역의 정보를 조회합니다",
        responses={
            200: MedicalServiceInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=service_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        parameters=[service_api_url_param],
        tags=["진료내역"],
        summary="진료내역 수정(put)",
        description="진료내역을 수정합니다. 현재 상태, 담당 스태프만 수정 가능합니다.",
        request=MedicalServiceInfoSerializer,
        responses={
            200: MedicalServiceInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=service_api_examples["mod"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        parameters=[service_api_url_param],
        tags=["진료내역"],
        summary="진료내역 수정(patch)",
        description="진료내역을 수정합니다. 현재 상태, 담당 스태프만 수정 가능합니다.",
        request=MedicalServiceInfoSerializer,
        responses={
            200: MedicalServiceInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=service_api_examples["mod"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        parameters=[service_api_url_param],
        tags=["진료내역"],
        summary="진료내역 삭제",
        description="지정된 진료내역을 삭제합니다.(진료내역이 완료상태라면 오류가 발생합니다.)",
        request=MedicalServiceInfoSerializer,
        responses={
            200: None,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
            406: OpenApiResponse(description="데이터 보호를 위해 삭제 불가"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance) -> None:
        """삭제처리

        완료된 내역이나 외래키 참조가 있다면 삭제 할 수 없다.
        """
        if instance.status == MedicalStageStatus.COMPLETE:
            raise exceptions.NotAcceptable(detail="완료 처리된 내역", code="protected_data")

        try:
            super().perform_destroy(instance)
        except ProtectedError as e:
            raise exceptions.NotAcceptable(detail="보호된 데이터", code="protected_data")
        except Exception as e:
            raise e
