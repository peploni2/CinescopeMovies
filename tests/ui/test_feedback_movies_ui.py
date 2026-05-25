import allure
import pytest
from playwright.sync_api import Page
from models.page_object_feedback import CinescopeMovieFeedback
from typing import Literal

@allure.epic("Тестирование movies_ui")
@allure.feature("Позитивные тесты movies_ui")
@pytest.mark.positive
@pytest.mark.ui
class TestFeedbackMovieUI:

    @allure.title("Авторизованный пользователь оставляет отзыв на фильм в UI")
    @allure.story("Корректность оставления отзыва в UI")
    def test_feedback_movie(self, auth_page_for_ui: Page, create_test_film: dict, feedback_text: str, random_rating: Literal[1, 2, 3, 4, 5]):
        with allure.step("Создание тестового фильма и логин юзером"):
            film_id = create_test_film["id"]

            feedback_page = CinescopeMovieFeedback(auth_page_for_ui)

        feedback_page.open(film_id)
        feedback_page.assert_feedback_text_area_is_enabled()
        feedback_page.enter_feedback(feedback_text, random_rating)
        feedback_page.assert_alert_was_pop_up("Отзыв успешно создан")
        feedback_page.assert_feedback_text_area_is_hidden()
        feedback_page.make_screenshot_and_attach_to_allure()

@allure.epic("Тестирование movies_ui")
@allure.feature("Негативные тесты movies_ui")
@pytest.mark.negative
@pytest.mark.ui
class TestNegativeFeedbackMovieUI:

    @allure.title("Авторизованный пользователь оставляет пустой отзыв на фильм в UI")
    @allure.story("Корректность оставления пустого отзыва в UI")
    def test_negative_feedback_movie(self,  auth_page_for_ui: Page, create_test_film: dict, random_rating: Literal[1, 2, 3, 4, 5]):
        with allure.step("Создание тестового фильма и логин юзером"):
            film_id = create_test_film["id"]

            feedback_page = CinescopeMovieFeedback(auth_page_for_ui)

        feedback_page.open(film_id)
        feedback_page.assert_feedback_text_area_is_enabled()
        feedback_page.enter_feedback("", random_rating)
        feedback_page.assert_alert_was_pop_up("Поле отзыва обязательно к заполнению")
        feedback_page.assert_feedback_text_area_is_enabled()
        feedback_page.assert_feedback_text_area_is_visible()
        feedback_page.make_screenshot_and_attach_to_allure()
