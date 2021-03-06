__all__ = ["UserChoicesTestCase", "UserModelTestCase"]

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.test import TestCase


user_model = get_user_model()
user_type = user_model.UserType
messenger_type = user_model.MessengerType


class UserChoicesTestCase(TestCase):
    """
    유저 모델에서 사용할 TextChoices 서브클래스 테스트
    IAMDTUser.UserType: Role 종류
    IAMDTUser.MessengerType: 메신저 종류
    """

    def setUp(self):
        pass

    def test_user_type(self):
        """Role 종류 Choices 확인"""
        self.assertEqual(["DOCTOR", "NURSE", "EMPLOYEE", "DEVELOPER"], user_type.names)
        self.assertEqual(["doctor", "nurse", "employee", "developer"], user_type.values)
        self.assertEqual(["수의사", "간호사", "직원", "개발자"], user_type.labels)

    def test_messenger_type(self):
        """메신저종류 Choices 확인"""
        self.assertEqual(
            ["DEFAULT", "KAKAOTALK", "FACEBOOK", "LINE", "TELEGRAM"],
            messenger_type.names,
        )
        self.assertEqual(
            ["-", "kakaotalk", "facebook", "line", "telegram"],
            messenger_type.values,
        )
        self.assertEqual(["없음", "카카오톡", "페이스북", "라인", "텔레그램"], messenger_type.labels)


class UserModelTestCase(TestCase):
    """
    유저 모델 테스트 클래스
    Django User Model을 확장해서 만들 IAMDTUser 모델 클래스를 테스트 한다.
    테스트할 추가 필드

    1. 스태프
        역할 - 의사 / 간호사 / 일반
            * IAMDTUser.UserType 서브클래스 사용(TextChoices)
                DOCTOR, NURSER, EMPLOYEE, DEVELOPER
        연락처

    2. 메신저
        메신저종류
        아이디
        사용여부"""

    fixtures = ["user.json"]

    def setUp(self) -> None:
        pass

    def test_info(self) -> None:
        """생성된 정보 확인"""
        user_info = {
            "username": "doctor1",
            "password": "1234",
            "role": "doctor",
            "is_staff": True,
            "phone": "01012345678",
            "messenger": "kakaotalk",
            "messenger_id": "doc1",
        }
        user = user_model.objects.get(username=user_info["username"])

        # username 및 비밀번호 확인
        self.assertTrue(check_password(user_info["password"], user.password))

        # 유저타입 확인
        self.assertEqual(user.role, user_info["role"])
        self.assertIn(user.role, user_type.values)

        # 연락처 확인
        self.assertEqual(user.phone, user_info["phone"])

        # 스태프 확인
        self.assertEqual(user.is_staff, user_info["is_staff"])

        # 메신저 정보 확인
        self.assertEqual(user.messenger, user_info["messenger"])
        self.assertEqual(user.messenger_id, user_info["messenger_id"])

    def test_filter(self) -> None:
        """유저모델 검색"""
        # 스태프로 생성된 유저수는 5명
        self.assertEqual(5, user_model.objects.filter(is_staff=True).count())
        # 슈퍼유저로 생성된 유저수는 1명
        self.assertEqual(1, user_model.objects.filter(is_superuser=True).count())

    def test_filter_role(self) -> None:
        """유저모델 role 검색"""
        self.assertEqual(1, user_model.objects.filter(role=user_type.DOCTOR).count())
        self.assertEqual(1, user_model.objects.filter(role=user_type.NURSE).count())
        self.assertEqual(
            1,
            user_model.objects.filter(role=user_type.EMPLOYEE).count(),
        )
        self.assertEqual(
            2,
            user_model.objects.filter(role=user_type.DEVELOPER).count(),
        )

    def test_filter_messenger(self) -> None:
        """유저모델 messenger 검색"""
        self.assertEqual(
            2,
            user_model.objects.filter(messenger=messenger_type.KAKAOTALK).count(),
        )
        self.assertEqual(
            0,
            user_model.objects.filter(messenger=messenger_type.TELEGRAM).count(),
        )

    def test_validation_role(self) -> None:
        """유저 role 검증"""
        user = user_model.objects.first()

        user.role = "asdf"
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.role = None
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_validation_phone(self) -> None:
        """유저 전화번호 검증"""
        user = user_model.objects.first()

        user.phone = "asdf"
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.phone = ""
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.phone = None
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_validation_messenger(self) -> None:
        """유저 messenger 검증"""
        user = user_model.objects.first()

        user.messenger = "asdf"
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.messenger = ""
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.messenger = None
        with self.assertRaises(ValidationError):
            user.full_clean()

        # User.MessengerType.DEFAULT
        user.messenger = messenger_type.DEFAULT
        user.full_clean()
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.messenger, messenger_type.DEFAULT)
