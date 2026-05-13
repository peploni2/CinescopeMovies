def multiply(a: int, b: int) -> int:
    return a * b

print(multiply("niger", 5))

def sum_numbers(numbers: list[int]) -> int:
    return sum(numbers)

# print(sum_numbers(["one", "two", "three"]))

from typing import Optional, Union

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

print(find_user(5))

def process_input(value: Union[int, str]):
    return f"Ты передал: {value}"

print(process_input(5))

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}"

user = User("Артем", 25)

print(user.greet())

def get_eve_numbers(numbers: list[int]):
    return [num for num in numbers if num % 2==0]
#
# print(get_eve_numbers(["niger"]))




