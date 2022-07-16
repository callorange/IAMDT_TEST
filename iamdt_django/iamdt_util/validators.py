"""
프로젝트에서 사용되는 validator 모음
"""
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$"
)
