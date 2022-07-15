"""
Patient Serializer 모듈
"""

__all__ = ["PatientInfoSerializer"]

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from iamdt.models import Patient


@extend_schema_serializer(
    component_name="PatientInfo",
    examples=[
        OpenApiExample(
            name="신규환자1",
            summary="환자정보 등록 성공",
            description="보호자 pk가 필요하며 동일 보호자에게 같은 이름의 환자는 등록 불가합니다.",
            value={"companion": 1, "name": "신규환자"},
            request_only=True,
        ),
        OpenApiExample(
            name="신규환자2",
            summary="환자정보 등록 실패(누락)",
            description="보호자 pk 혹은 이름은 모두 필수 값 입니다.",
            value={"name": "customer1"},
            request_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="신규환자3",
            summary="환자정보 등록 실패(중복)",
            description="보호자 pk + 환자이름 은 중복될 수 없습니다.(테스트시 기존 정보를 확인하세요)",
            value={"companion": 1, "name": "환자1"},
            request_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="환자정보1",
            summary="환자정보 조회",
            description="read_only 필드인 id, created_at, updated_at가 포함 됩니다.",
            value={
                "id": "1",
                "name": "고객1",
                "phone": "01022223333",
                "created_at": "2022-07-13T10:28:31.680Z",
                "updated_at": "2022-07-13T10:30:21.885Z",
            },
            response_only=True,
        ),
        OpenApiExample(
            name="환자정보2",
            summary="환자정보 추가/수정",
            description="추가/수정시에는 제출된 데이터만 확인용으로 응답됩니다.",
            value={"name": "고객1", "phone": "01022223333"},
            response_only=True,
        ),
    ],
)
class PatientInfoSerializer(serializers.ModelSerializer):
    """환자정보 시리얼라이저"""

    class Meta:
        model = Patient
        fields = ["id", "name", "companion", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        validators = [
            UniqueTogetherValidator(
                queryset=Patient.objects.all(), fields=["companion", "name"]
            )
        ]
