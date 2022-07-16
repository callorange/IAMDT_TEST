"""
API Permission 모듈
"""

from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """superuser라면 전부 허용"""

    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_superuser


class ObjOwnerOrReadOnly(permissions.BasePermission):
    """지정된 유저만와 superuser만 object 편집 허용

    1. object_owner_id에 지정한 필드와 request.user.id를 비교.
    2. is_superuser = True 라면 허용
    3. 그외 ReadONly

    Examples
    --------
    object_owner_id = "id"
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # 읽기는 모두 허용한다(GET, HEAD, OPTIONS 메소드)
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True

        owner_id = getattr(obj, getattr(view, "object_owner_id"))
        return owner_id == request.user.id
