from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from iamdt.models import User


@admin.register(User)
class IAMDTUserAdmin(UserAdmin):
    """유저정보 어드민

    유저 모델을 AbAbstractUser를 상속받았으므로 UserAdmin을 상속받아 구현한다.
    """

    fieldsets = UserAdmin.fieldsets + (
        (
            "추가 개인정보",
            {
                "fields": [
                    "role",
                    "phone",
                    "messenger",
                    "messenger_id",
                ]
            },
        ),
    )
