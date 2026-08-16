import allure
from selenium.common.exceptions import TimeoutException

from constants import BASE_URL, ORDER_ATTEMPT_TIMEOUT, ORDER_TIMEOUT
from locators import HeaderLocators, MainPageLocators
from pages.base_page import BasePage
from pages.login_page import LoginPage


class MainPage(BasePage):
    URL = f"{BASE_URL}/"

    @allure.step("Открыть конструктор")
    def open(self):
        self.open_url(self.URL)
        self.visible(MainPageLocators.PAGE_TITLE)
        self.wait_no_visible_elements(MainPageLocators.MODAL_OVERLAY)
        return self

    def is_opened(self):
        return self.is_current_url(self.URL) and self.is_visible(
            MainPageLocators.PAGE_TITLE
        )

    @allure.step("Перейти в конструктор через шапку")
    def click_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)
        self.wait_url(self.URL)

    @allure.step("Перейти в ленту заказов через шапку")
    def click_feed(self):
        self.click(HeaderLocators.FEED_LINK)
        self.wait_url(f"{BASE_URL}/feed")

    @allure.step("Открыть детали ингредиента")
    def open_ingredient_details(self):
        self.click(MainPageLocators.BUN_CARD)
        self.visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def ingredient_modal_is_open(self):
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def ingredient_modal_is_closed(self):
        return self.no_visible_elements(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def close_modal(self):
        self.close_visible_modal(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_invisible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def ingredient_counter(self, card_locator):
        return int(self.child_text(card_locator, MainPageLocators.INGREDIENT_COUNTER))

    def sauce_counter(self):
        return self.ingredient_counter(MainPageLocators.SAUCE_CARD)

    @allure.step("Добавить ингредиент и дождаться увеличения счётчика")
    def add_ingredient(self, card_locator):
        before = self.ingredient_counter(card_locator)
        self.drag_and_drop(card_locator, MainPageLocators.BASKET)
        try:
            self.wait_for(lambda: self.ingredient_counter(card_locator) > before, 5)
        except TimeoutException:
            self.html5_drag_and_drop(card_locator, MainPageLocators.BASKET)
            self.wait_for(
                lambda: self.ingredient_counter(card_locator) > before,
                ORDER_TIMEOUT,
            )
        return self.ingredient_counter(card_locator)

    def add_sauce(self):
        return self.add_ingredient(MainPageLocators.SAUCE_CARD)

    @allure.step("Собрать бургер")
    def assemble_burger(self):
        self.add_ingredient(MainPageLocators.BUN_CARD)
        self.add_ingredient(MainPageLocators.FILLING_CARD)

    @allure.step("Оформить заказ")
    def create_order(self):
        def real_order_number():
            for text in self.visible_texts(MainPageLocators.ORDER_NUMBER):
                if text.isdigit() and text != "9999":
                    return int(text)
            return False

        last_error = None
        for attempt in range(2):
            with allure.step(f"Попытка оформления заказа №{attempt + 1}"):
                self.click(MainPageLocators.ORDER_BUTTON)
                try:
                    return self.wait_for(real_order_number, ORDER_ATTEMPT_TIMEOUT)
                except TimeoutException as error:
                    last_error = error
                    self.close_visible_modal(MainPageLocators.MODAL_CLOSE_BUTTON)
                    self.wait_no_visible_elements(MainPageLocators.ORDER_NUMBER)

        raise last_error

    @allure.step("Закрыть окно оформленного заказа")
    def close_order_modal(self):
        self.close_visible_modal(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_no_visible_elements(
            MainPageLocators.ORDER_NUMBER,
            ORDER_TIMEOUT,
        )

    @allure.step("Войти и оформить заказ")
    def create_order_for_user(self, email, password):
        self.as_page(LoginPage).open().login(email, password)
        self.assemble_burger()
        order_number = self.create_order()
        self.close_order_modal()
        return order_number
