from playwright.sync_api import sync_playwright, Page

class CinescopeRegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://dev-cinescope.coconutqa.ru/register"

        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")

        self.full_name_input = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.repeat_password_input = page.get_by_role("textbox", name="Повторите пароль")

        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.sign_button = page.locator("form").get_by_role("link", name="Войти")

    def go_to_home_page(self):
        self.home_button.click()
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")

    def go_to_all_movies(self):
        self.all_movies_button.click()
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")

    def open(self):
        self.page.goto(self.url)

    def enter_full_name(self, full_name: str):
        self.full_name_input.fill(full_name)

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def enter_repeat_password(self, password: str):
        self.repeat_password_input.fill(password)

    def click_register_button(self):
        self.register_button.click()

    def register(self, full_name: str, email: str, password:str, confirm_password:str):
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_repeat_password(confirm_password)
        self.click_register_button()

    def wait_redirect_to_login_page(self):
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/login")
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/login", "Редирект на домашнюю страницу не произошел"

    def check_allert(self):
        notification_locator = self.page.get_by_text("Подтвердите свою почту")
        notification_locator.wait_for(state="visible")

        assert notification_locator.is_visible(), "Уведомление не появилось"

        notification_locator.wait_for(state="hidden")
        assert not notification_locator.is_visible(), "Уведомление не исчезло"

class CinescopeLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://dev-cinescope.coconutqa.ru/login"

        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль")
        self.login_button = page.locator("form").get_by_role("button", name="Войти")
        self.register_button = page.get_by_role("link", name="Зарегистрироваться")

    def go_to_home_page(self):
        self.home_button.click()
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")

    def go_to_all_movies(self):
        self.all_movies_button.click()
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")

    def open(self):
        self.page.goto("https://dev-cinescope.coconutqa.ru/login")

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def wait_redirect_to_home_page(self):
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/", "Редиректа не было"

    def check_allert(self):
        notification_locator = self.page.get_by_text("Вы вошли в аккаунт")
        notification_locator.wait_for(state="visible")
        assert notification_locator.is_visible(), "Уведомление не появилось"

        notification_locator.wait_for(state="hidden")
        assert not notification_locator.is_visible()





