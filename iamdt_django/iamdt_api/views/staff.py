"""
Staff API View
"""

__all__ = ["StaffList", "StaffDetail"]

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError, Subquery
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, permissions, exceptions

from iamdt.models import MedicalRegister, MedicalService
from iamdt_api import permissions as perms
from iamdt_api.scheme import PAGINATION_QUERY_SCHEME
from iamdt_api.scheme.medical_service import SERVICE_API_EXAMPLES
from iamdt_api.scheme.staff import staff_api_examples
from iamdt_api.serializers import StaffInfoSerializer, StaffAddSerializer
from iamdt_api.serializers.medical_register import MedicalRegisterInfoSerializer
from iamdt_api.serializers.medical_service import MedicalServiceInfoSerializer

user_model = get_user_model()


class StaffList(generics.ListCreateAPIView):
    """Staff 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = user_model.objects.filter(is_staff=True).order_by("-id")

    def get_serializer_class(self):
        """post일때는 등록용 시리얼라이저를 반환하도록 한다"""
        if self.request.method == "POST":
            return StaffAddSerializer
        return StaffInfoSerializer

    @extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 검색",
        description="병원의 스태프 리스트를 검색합니다",
        responses={
            200: StaffInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
        examples=staff_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 등록",
        description="병원의 신규 스태프를 등록합니다",
        request=StaffAddSerializer,
        responses={
            200: StaffAddSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        examples=staff_api_examples["add"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """is_staff를 강제로 추가 시킨다"""
        serializer.save(is_staff=True)


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser, perms.ObjOwnerOrReadOnly]
    queryset = get_user_model().objects.filter(is_staff=True)
    serializer_class = StaffInfoSerializer

    lookup_url_kwarg = "id"
    lookup_field = "id"

    object_owner_id = "id"

    @extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 정보조회",
        description="지정된 스태프의 정보를 조회합니다",
        responses={
            200: StaffInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=staff_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 정보수정(put)",
        description="지정된 스태프의 정보를 수정합니다",
        request=StaffInfoSerializer,
        responses={
            200: StaffInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=staff_api_examples["mod"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 정보수정(patch)",
        description="지정된 스태프의 정보를 수정합니다",
        request=StaffInfoSerializer,
        responses={
            200: StaffInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=staff_api_examples["mod"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 삭제",
        description="지정된 스태프를 삭제합니다.(해당 스태프가 추가한 데이터가 있다면 오류가 발생합니다.)",
        request=StaffInfoSerializer,
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


class StaffSchedule(generics.ListAPIView):
    """스태프가 담당중인 의료내역"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = MedicalRegister.objects.order_by("-id")
    serializer_class = MedicalRegisterInfoSerializer

    def get_queryset(self):
        """url kwargs에 따라 진료접수 쿼리셋 반환"""
        queryset = (
            super()
            .get_queryset()
            .filter(
                id__in=MedicalService.objects.filter(
                    id__in=MedicalService.staff.through.objects.filter(
                        staff=self.kwargs["id"]
                    ).values("detail")
                ).values("register")
            )
        )
        return queryset

    @extend_schema(
        tags=["병원 스태프"],
        summary="스태프의 진료내역 검색",
        description="지정된 스태프의 진료내역 리스트를 검색합니다",
        responses={
            200: MedicalServiceInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
        examples=SERVICE_API_EXAMPLES["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
