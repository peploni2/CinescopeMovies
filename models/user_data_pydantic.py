from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enums.roles import Roles
from venv import logger
from enum import Enum

class UserData(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length= 8, description="Пароль должен содержать не меньше 8 символов")
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    def check_email(cls, email: str) -> str:

        if not "@" in email:
            raise ValueError("Некорректный email")
        return email




def test_user_data(registration_user_data):
    user_data = UserData(**registration_user_data)

    logger.info(f"{user_data.email=} {user_data.fullName=} {user_data.password=} {user_data.passwordRepeat=} {user_data.roles=} {user_data.banned=} {user_data.verified=}")

def test_updated_user_data(test_user, creation_user_data):
    user_data = UserData(**test_user)
    json_test_user = user_data.model_dump_json(exclude_unset = True)
    logger.info(f"{user_data.email=} {user_data.fullName=} {user_data.password=} {user_data.passwordRepeat=} {user_data.roles=} {user_data.banned=} {user_data.verified=}")
    print(json_test_user)

    user_data = UserData(**creation_user_data)
    json_creation_user_data = user_data.model_dump_json()
    logger.info(f"{user_data.email=} {user_data.fullName=} {user_data.password=} {user_data.passwordRepeat=} {user_data.roles=} {user_data.banned=} {user_data.verified=}")
    print(json_creation_user_data)
