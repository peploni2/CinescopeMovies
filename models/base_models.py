from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List
import datetime
import re
from pydantic import BaseModel, Field, field_validator
from enums.roles import Roles
from enum import Enum

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Пароли должны совпадать")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value:str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value

class Location(str, Enum):
    MSK = "MSK"
    SPB = "SPB"

class FilmData(BaseModel):
    name: str
    imageUrl: str
    price: int = Field(gt=0)
    description: str
    location: Location
    published: bool
    genreId: int

class CreatedFilmResponse(BaseModel):
    id: int
    name: str
    price: int = Field(gt = 0)
    description: str
    imageUrl: str
    location: Location
    published: bool
    genreId: int
    genre: Dict[str, str]
    createdAt: str
    rating: int

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value

class Review(BaseModel):
    userId: str
    rating: int
    text: str
    createdAt: str
    user: Dict[str, str]

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value

class GetFilmResponse(BaseModel):
    id: int
    name: str
    price: int = Field(gt = 0)
    description: str
    imageUrl: str
    location: Location
    published: bool
    genreId: int
    genre: Dict[str, str]
    createdAt: str
    rating: int
    reviews: List[Review] = Field(default_factory=list)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value