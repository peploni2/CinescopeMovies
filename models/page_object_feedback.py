from playwright.sync_api import sync_playwright, Page, Locator, expect
import allure
from models.page_action_model import BasePage
from typing import Literal
from utils.data_generator import DataGenerator

class CinescopeMovieFeedback(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}movies/"

        self.feedback_text_area_input = page.get_by_role("textbox", name="Написать отзыв")
        self.push_button = page.get_by_role("button", name="Отправить")
        self.rating_selector = page.get_by_role("combobox")

    def open(self, film_id):
        self.open_url(f"{self.url}{film_id}")

    @allure.step("Выбор рейтинга")
    def select_rating(self, rating: Literal[1, 2, 3, 4, 5]):
        self.rating_selector.click()
        self.page.get_by_role("option", name=str(rating)).click()

        expect(self.rating_selector).to_contain_text(str(rating))

    @allure.step("Отправка отзыва")
    def enter_feedback(self,random_text: str = "", rating: Literal[1, 2, 3, 4, 5] = 5):

        self.enter_text_to_element(self.feedback_text_area_input, random_text)
        self.select_rating(rating)
        self.click_element(self.push_button)

    def сheck_alert_was_pop_up(self, pop_up_text: str):
        self.check_pop_up_element_with_text(pop_up_text)

    @allure.step("Поверка что поле ввода текста в отзыве доступно")
    def сheck_feedback_text_area_is_enabled(self):
        expect(self.feedback_text_area_input).to_be_enabled()

    @allure.step("Поверка что поле ввода текста в отзыве скрыто")
    def сheck_feedback_text_area_is_hidden(self):
        expect(self.feedback_text_area_input).to_be_hidden()

    @allure.step("Поверка что поле ввода текста в отзыве видно")
    def сheck_feedback_text_area_is_visible(self):
        expect(self.feedback_text_area_input).to_be_visible()



