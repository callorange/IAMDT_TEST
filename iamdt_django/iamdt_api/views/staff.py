"""
Staff API View
"""

__all__ = ["StaffList", "StaffDetail"]

from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework import generics, permissions

from iamdt_api import permissions as perms
from iamdt_api.serializers import StaffSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 검색",
        description="병원의 스태프 리스트를 검색합니다",
        responses={
            200: StaffSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=[
            OpenApiParameter(
                "page",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="조회할 페이지",
            ),
            OpenApiParameter(
                "page_size",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="한페이지당 레코드 최대 갯수",
            ),
        ],
    ),
    post=extend_schema(
        tags=["병원 스태프"],
        summary="병원 스태프 등록",
        description="병원의 신규 스태프를 등록합니다",
        request=StaffSerializer,
        responses={
            200: StaffSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
    ),
)
class StaffList(generics.ListCreateAPIView):
    """Staff 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = get_user_model().objects.filter(is_staff=True)
    serializer_class = StaffSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StaffSerializer
        return StaffSerializer

    def perform_create(self, serializer):
        serializer.save(is_staff=True)


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser, perms.ObjOwnerOrReadOnly]
    queryset = get_user_model().objects.filter(is_staff=True)
    serializer_class = StaffSerializer

    lookup_url_kwarg = "id"

    object_owner_id = "id"
