"""
Customer Api View
"""

__all__ = ["CustomerList", "CustomerDetail"]

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

from iamdt.models import Customer
from iamdt_api.scheme import PAGINATION_QUERY_SCHEME
from iamdt_api.serializers import CustomerInfoSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["고객정보"],
        summary="고객정보 검색",
        description="고객정보 리스트를 검색합니다",
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
    ),
    post=extend_schema(
        tags=["고객정보"],
        summary="고객정보 등록",
        description="신규 고객을 등록합니다.",
        request=CustomerInfoSerializer,
        responses={
            200: CustomerInfoSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
    ),
)
class CustomerList(generics.ListCreateAPIView):
    """Staff 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = Customer.objects.order_by("-id")
    serializer_class = CustomerInfoSerializer


# 고객상세 url path kwargs
url_kwargs = OpenApiParameter(
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


@extend_schema_view(
    get=extend_schema(
        parameters=[url_kwargs],
        tags=["고객정보"],
        summary="고객정보 조회",
        description="지정된 고객의 정보를 조회합니다",
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
    ),
    put=extend_schema(
        parameters=[url_kwargs],
        tags=["고객정보"],
        summary="고객정보 정보수정(put)",
        description="지정된 고객의 정보를 수정합니다",
        request=CustomerInfoSerializer,
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
    ),
    patch=extend_schema(
        parameters=[url_kwargs],
        tags=["고객정보"],
        summary="고객정보 정보수정(patch)",
        description="지정된 고객의 정보를 수정합니다",
        request=CustomerInfoSerializer,
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
    ),
    delete=extend_schema(
        parameters=[url_kwargs],
        tags=["고객정보"],
        summary="고객정보 삭제",
        description="지정된 고객정보룰 삭제합니다.(해당 고객의 접수내역등이 있다면 오류가 발생합니다.)",
        request=CustomerInfoSerializer,
        responses={
            200: None,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
            406: OpenApiResponse(description="데이터 보호를 위해 삭제 불가"),
        },
    ),
)
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerInfoSerializer

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
