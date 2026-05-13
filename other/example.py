import pytest

@pytest.mark.parametrize("input_data,expected", [(1, 2), (2, 4), (3,6)])
def test_multiply_by_two(input_data, expected):
    assert input_data * 2 == expected

@pytest.mark.parametrize("parameter_name", ["value1", "value2"])
class TestParametrizedClass:
    def test_first(self, parameter_name):
        print(f"Test 1 прогон: {parameter_name}")
        assert True

    def test_second(self, parameter_name):
        print(f"Test 2 прогон: {parameter_name}")
        assert True

@pytest.mark.parametrize("param_a, param_b", [
    ("a1", "b1"),
    ("a2", "b2")
])
class TestMultipleParams:
    def test_params_combination(self, param_a, param_b):
        print(f"1 test: {param_a} and {param_b}")

    def test_another_method(self, param_a, param_b):
        combined = f"{param_a} - {param_b}"
        print(f"2 test: {combined}")
        assert len(combined) > 2

@pytest.mark.parametrize("class_param", ["c1", "c2"])
class TestCombinedParametrization:

    @pytest.mark.parametrize("method_param", ["m1", "m2", "m3"])
    def test_combination(self, class_param, method_param):
        print(f"Тест 1 параметризацией класса ={class_param} и метода ={method_param}")
        assert True

    def test_only_class_param(self, class_param):
        print(f"Тест 2 параметризацией только класса = {class_param}")
        assert True

@pytest.mark.parametrize("feature_flag,platform", [
    ("feature_a", "windows"),
    ("feature_a", "mac"),
    ("feature_b", "windows"),
    pytest.param("feature_b", "mac", marks=pytest.mark.skip(reason="Not supported on Mac"))
])
class TestFeatures:

    def test_feature_availability(self, feature_flag, platform):
        print(f"Testing {feature_flag} on {platform}")
        assert True

from resources.user_creds import SuperAdminCreds

@pytest.mark.parametrize("email, password, expected_status", [
    (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", 200),
    ("test_login1@email.com", "asdqwe123Q!", 401),
    ("", "password", 401),
], ids = ["Admin login", "Invalid user", "Empty username"])
def test_login(email, password, expected_status, api_manager):
    login_data = {
        "email": email,
        "password": password
    }
    api_manager.auth_api.login_user(login_data=login_data, expected_status = expected_status)

def add(a: int, b: int) -> int:
    return a+b

from typing import List

def sum_numbers(number: List[int]) -> int:
    return sum(number)

from typing import Dict, Tuple, Set

def user_info() -> Dict[str, int]:
    return {"age": 25, "height": 180}

def get_coordinate() -> Tuple[float, float]:
    return (55.6634, 37.5433)

def unique_numbers(numbers: Set[int]) -> Set[int]:
    return set(numbers)

def func(numbers: list[int]) -> list[int]:
    return numbers

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"

from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

from typing import Union

def process_input(value: Union[int, str]) -> str:
    return f"Ты передал {value}"

@pytest.mark.smoke
def test_addition():
    assert 1 + 1 == 2

@pytest.mark.regression
def test_subtraction():
    assert 5-3 == 2

@pytest.mark.api
def test_multiplication():
    assert 2 * 3 == 6

@pytest.mark.slow
def test_division():
    assert 10/2==5

