from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from iamdt.models import (
    User,
    Customer,
    Patient,
    MedicalRegister,
    MedicalService,
    MedicalStaff,
)


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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "companion",
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(MedicalRegister)
class MedicalRegisterAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")


class StaffInlineAdmin(admin.StackedInline):
    model = MedicalService.staff.through
    extra = 0


@admin.register(MedicalService)
class MedicalServiceAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "register",
        "stage",
        "status",
        "creator",
        "created_at",
        "updated_at",
    )
    fields = (
        "patient",
        "register",
        "stage",
        "status",
        "creator",
        "created_at",
        "updated_at",
    )

    inlines = (StaffInlineAdmin,)
    readonly_fields = ("created_at", "updated_at")


@admin.register(MedicalStaff)
class MedicalStaffAdmin(admin.ModelAdmin):
    list_display = ("detail", "staff", "created_at")
    readonly_fields = ("created_at",)
