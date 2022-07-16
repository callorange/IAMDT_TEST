__all__ = ["ApiPageNumberPagination"]

from rest_framework.pagination import PageNumberPagination


class ApiPageNumberPagination(PageNumberPagination):
    """
    DRF PageNumberPagination 상속받은 클래스
    기본 속성만 바꿨다
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000
