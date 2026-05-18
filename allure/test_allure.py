import allure
import pytest

@allure.title("Проверка сложения двух числе")
@allure.description("Тест проверяет, что сумма двух чисел вычисляется корректно")
def test_addition():
    with allure.step("Проверка суммы 2+2"):
        assert 2+2 == 4

    with allure.step("проверка суммы 3+2"):
        assert 2+2 == 5

@allure.step("Проверка сложения чисел {a} и {b}")
def check_addition(a, b, expected):
    with allure.step(f"Сложение {a} и {b}"):
        result = a + b
    with allure.step(f"Проверка результата {result} == {expected}"):
        assert result == expected

def test_additio():
    check_addition(2, 2, 4)
    check_addition(3, 5, 8)