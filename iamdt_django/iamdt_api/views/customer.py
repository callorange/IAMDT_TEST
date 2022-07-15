"""
Customer Api View
"""

__all__ = ["CustomerList", "CustomerDetail"]

from django.db.models import ProtectedError
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, permissions, exceptions

from iamdt.models import Customer
from iamdt_api.scheme import PAGINATION_QUERY_SCHEME
from iamdt_api.scheme.customer import customer_api_url_param, customer_api_examples
from iamdt_api.serializers import CustomerInfoSerializer


class CustomerList(generics.ListCreateAPIView):
    """Staff 검색/등록 View"""

    permission_classes = [permissions.IsAdminUser]  # is_staff 만
    queryset = Customer.objects.order_by("-id")
    serializer_class = CustomerInfoSerializer

    @extend_schema(
        tags=["고객정보"],
        summary="고객정보 검색",
        description="고객정보 리스트를 검색합니다",
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        parameters=PAGINATION_QUERY_SCHEME,
        examples=customer_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["고객정보"],
        summary="고객정보 등록",
        description="신규 고객을 등록합니다.",
        request=CustomerInfoSerializer,
        responses={
            200: CustomerInfoSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            403: OpenApiResponse(description="인증 없는 액세스"),
        },
        examples=customer_api_examples["add"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerInfoSerializer

    lookup_url_kwarg = "id"

    @extend_schema(
        parameters=[customer_api_url_param],
        tags=["고객정보"],
        summary="고객정보 조회",
        description="지정된 고객의 정보를 조회합니다",
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=customer_api_examples["read"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        parameters=[customer_api_url_param],
        tags=["고객정보"],
        summary="고객정보 정보수정(put)",
        description="지정된 고객의 정보를 수정합니다",
        request=CustomerInfoSerializer,
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=customer_api_examples["mod"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        parameters=[customer_api_url_param],
        tags=["고객정보"],
        summary="고객정보 정보수정(patch)",
        description="지정된 고객의 정보를 수정합니다",
        request=CustomerInfoSerializer,
        responses={
            200: CustomerInfoSerializer,
            403: OpenApiResponse(description="인증 없는 액세스"),
            404: OpenApiResponse(description="찾을 수 없는 데이터"),
        },
        examples=customer_api_examples["mod"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        parameters=[customer_api_url_param],
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
    )
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            raise exceptions.NotAcceptable(
                detail="Unable to delete for data protection", code="protected_data"
            )
        except Exception as e:
            raise e
