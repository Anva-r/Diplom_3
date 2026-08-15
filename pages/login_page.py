import allure

from constants import BASE_URL
from locators import LoginPageLocators, MainPageLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = f"{BASE_URL}/login"

    def open(self):
        self.open_url(self.URL)
        self.visible(LoginPageLocators.PAGE_TITLE)
        self.wait_no_visible_elements(MainPageLocators.MODAL_OVERLAY)
        return self

    @allure.step("Войти как тестовый пользователь")
    def login(self, email, password):
        self.fill(LoginPageLocators.EMAIL_INPUT, email)
        self.fill(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)
        self.wait_url(f"{BASE_URL}/")
        self.visible(MainPageLocators.PAGE_TITLE)
        self.wait_no_visible_elements(MainPageLocators.MODAL_OVERLAY)
