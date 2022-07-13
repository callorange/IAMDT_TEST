from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.test import TestCase


# Create your tests here.

test_user_info = [
    {
        "username": "doctor1",
        "password": "d1111",
        "role": "doctor",
        "is_staff": True,
        "phone": "01012345678",
        "messenger": "kakaotalk",
        "messenger_id": "doc1",
    },
    {
        "username": "nurse1",
        "password": "n1111",
        "role": "nurse",
        "is_staff": True,
        "phone": "01012345678",
        "messenger": "kakaotalk",
        "messenger_id": "nurse1",
    },
    {
        "username": "employee1",
        "password": "e1111",
        "role": "employee",
        "is_staff": True,
        "phone": "01012345678",
        "messenger": "facebook",
        "messenger_id": "e1",
    },
    {
        "username": "dev1",
        "password": "d1111",
        "role": "developer",
        "is_staff": True,
        "is_superuser": True,
        "phone": "01012345678",
        "messenger": "line",
        "messenger_id": "dev11",
    },
]

user_model = get_user_model()
user_type = user_model.UserType
messenger_type = user_model.MessengerType


class IAMDTUserChoicesTestCase(TestCase):
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
            ["", "kakaotalk", "facebook", "line", "telegram"],
            messenger_type.values,
        )
        self.assertEqual(["없음", "카카오톡", "페이스북", "라인", "텔레그램"], messenger_type.labels)


class IAMDTUserModelTestCase(TestCase):
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

    def setUp(self):
        # 유저 생성
        for user_info in test_user_info:
            user = user_model.objects.create_user(**user_info)

    def test_create_user(self):
        """생성된 정보 확인"""
        user_info = test_user_info[0]
        user = user_model.objects.get(username=user_info["username"])

        # username 및 비밀번호 확인
        self.assertTrue(check_password(user_info["password"], user.password))

        # 유저타입 확인
        self.assertEqual(user.role, user_info["role"])
        self.assertIn(user.role, user_type.values)

        # 연락처 확인
        self.assertEqual(user.phone, user_info["phone"])

        # 스태프/슈퍼유저 확인
        self.assertEqual(user.is_staff, user_info["is_staff"])
        if user_info.get("is_superuser", None):
            self.assertEqual(user.is_superuser, user_info["is_superuser"])

        # 메신저 정보 확인
        self.assertEqual(user.messenger, user_info["messenger"])
        self.assertEqual(user.messenger_id, user_info["messenger_id"])

    def test_user_model_filter(self):
        """유저모델 검색 기능 테스트"""
        # 스태프로 생성된 유저수는 4명
        self.assertEqual(4, user_model.objects.filter(is_staff=True).count())

        # 슈퍼유저로 생성된 유저수는 1명
        self.assertEqual(1, user_model.objects.filter(is_superuser=True).count())

        # Role 검색
        self.assertEqual(1, user_model.objects.filter(role=user_type.DOCTOR).count())
        self.assertEqual(1, user_model.objects.filter(role=user_type.NURSE).count())
        self.assertEqual(
            1,
            user_model.objects.filter(role=user_type.EMPLOYEE).count(),
        )
        self.assertEqual(
            1,
            user_model.objects.filter(role=user_type.DEVELOPER).count(),
        )

        # messenger로 검색
        self.assertEqual(
            2,
            user_model.objects.filter(messenger=messenger_type.KAKAOTALK).count(),
        )
        self.assertEqual(
            0,
            user_model.objects.filter(messenger=messenger_type.TELEGRAM).count(),
        )

    def test_user_info_validation(self):
        """유저 정보 변경 검증"""
        user_info = test_user_info[2]
        user = user_model.objects.get(username=user_info["username"])

        # 전화번호 잘못된 값 지정시 검증 실패
        user.refresh_from_db()
        user.phone = "asdf"
        with self.assertRaises(ValidationError):
            user.full_clean()

        # role 잘못된 값 지정시 검증 실패
        user.refresh_from_db()
        user.role = "asdf"
        with self.assertRaises(ValidationError):
            user.full_clean()

        # messenger 잘못된 값 지정시 검증 실패
        user.refresh_from_db()
        user.messenger = "asdf"
        with self.assertRaises(ValidationError):
            user.full_clean()

        # 정상값을 지정하고 메신저 타입이 변경되었는지 확인
        user.refresh_from_db()
        user.messenger = messenger_type.TELEGRAM
        user.full_clean()
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.messenger, messenger_type.TELEGRAM)
