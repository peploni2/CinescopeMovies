from pydantic import BaseModel
from venv import logger

class User(BaseModel):
    name: str
    age: int
    adult: bool

def get_user():
    return {
        "name": "Alice",
        "age": 25,
        "adult": "true"
    }

def test_user_data():
    user = User(**get_user())
    assert user.name == "Alice"
    logger.info(f"{user.name=} {user.age=} {user.adult=}")

from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
from venv import logger

class PostgresClient:
    @staticmethod
    def get(key: str):
        return None

class Card(BaseModel):
    pan: str = Field(..., min_length=16, max_length=16, description="Номер карты")
    cvc: str = Field(..., min_lenght=3, max_lenght=3)

    @field_validator("pan")
    def check_pan(cls, value: str) -> str:
        if PostgresClient.get(f"card_by_pan_{value}") is None:
            raise ValueError("Такой карты не существует")
        return value

def test_field_validator():
    try:
        card = Card(pan="1111222233334444", cvc="123")
        logger.info(card)
    except ValidationError as e:
        logger.info(f"Ошибка валидации: {e}")
        raise