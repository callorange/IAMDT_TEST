"""
MedicalService Serializer 모듈
"""

__all__ = ["MedicalServiceAddSerializer", "MedicalServiceInfoSerializer"]

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from iamdt.models import MedicalService
from iamdt.models.choices import MedicalStage, POSSIBLE_STAGES
from iamdt_api.scheme.medical_service import service_api_examples
from iamdt_api.serializers.staff import SimpleStaffField


@extend_schema_serializer(
    component_name="MedicalServiceAdd", examples=service_api_examples["add"]
)
class MedicalServiceAddSerializer(serializers.ModelSerializer):
    """진료내역 등록용 시리얼라이저

    환자, 진료단계, 담당스태프 3개 정보만 입력받는다
    """

    stage_display = serializers.CharField(source="get_stage_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    staff = SimpleStaffField(many=True, queryset=get_user_model().objects.all())

    class Meta:
        model = MedicalService
        fields = [
            "id",
            "patient",
            "register",
            "stage",
            "stage_display",
            "status",
            "status_display",
            "creator",
            "staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            # "patient",
            "register",
            # "stage",
            "status",
            "creator",
            # "staff",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """데이터 검증"""
        self._get_last_service(data)  # 마지막 단계를 찾는다.
        self._get_register()  # 마지막 접수번호를 찾는다.

        # 기존 진료에 이어서 진행하는가?
        if self._register_id:
            self._validate_possible_stage(data)  # 이행가능한 단계인지?

        return data

    def _get_last_service(self, data):
        """마지막 진료 정보를 찾는다"""
        obj = (
            MedicalService.objects.select_related("register")
            .filter(patient=data["patient"])
            .order_by("id")
            .last()
        )
        self._last_service = obj

    def _get_register(self):
        """마지막 진료정보에서 접수번호를 찾아 넣는다"""
        # 마지막 진료번호
        self._register_id = None

        # 마지막 진료정보 있고 퇴원이 아니면 해당 진료를 이어서 한다
        if self._last_service and self._last_service.stage != MedicalStage.DISCHARGE:
            self._register_id = self._last_service.register.id

    def _validate_possible_stage(self, data) -> None:
        """기존 단계에서 이어갈 수 있는 단계 인가?"""
        possible = POSSIBLE_STAGES[self._last_service.stage]
        if data["stage"] not in possible:

            raise serializers.ValidationError(
                f"'{MedicalStage(self._last_service.stage).label}'에서 "
                f"'{MedicalStage(data['stage']).label}'로 진행 할 수 없습니다"
            )


@extend_schema_serializer(
    component_name="MedicalServiceInfo", examples=service_api_examples["mod"]
)
class MedicalServiceInfoSerializer(serializers.ModelSerializer):
    """진료내역 정보 시리얼라이저"""

    stage_display = serializers.CharField(source="get_stage_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    staff = SimpleStaffField(many=True, queryset=get_user_model().objects.all())

    class Meta:
        model = MedicalService
        fields = [
            "id",
            "patient",
            "register",
            "stage",
            "stage_display",
            "status",
            "status_display",
            "creator",
            "staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "patient",
            "register",
            "stage",
            # "status",
            "creator",
            # "staff",
            "created_at",
            "updated_at",
        ]
