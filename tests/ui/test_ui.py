import allure
import pytest
import time
from models.page_action_model import CinescopeLoginPage, CinescopeRegisterPage
from utils.data_generator import DataGenerator

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestLoginPage:

    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, page, registered_user, test_user):
        login_page = CinescopeLoginPage(page)

        login_page.open()

        login_page.login(registered_user["email"], test_user.password)

        login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
        login_page.assert_allert_was_pop_up()

        time.sleep(5)

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page):
        #Подготовка данных для регистрации
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopeRegisterPage(page) # Создаем объект страницы регистрации cinescope
        register_page.open()
        register_page.register(f"PlaywrightTest {random_name}", random_email, random_password, random_password)# Выполняем регистрацию

        register_page.assert_was_redirect_to_login_page()  # Проверка редиректа на страницу /login
        register_page.make_screenshot_and_attach_to_allure() # Прикрепляем скриншот
        register_page.assert_allert_was_pop_up() # Проверка появления и исчезновения алерта

        # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
        time.sleep(5)

