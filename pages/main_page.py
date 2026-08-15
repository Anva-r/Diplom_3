import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from constants import BASE_URL, ORDER_ATTEMPT_TIMEOUT, ORDER_TIMEOUT
from locators import HeaderLocators, MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    URL = f"{BASE_URL}/"

    @allure.step("Открыть конструктор")
    def open(self):
        self.open_url(self.URL)
        self.visible(MainPageLocators.PAGE_TITLE)
        self.wait_no_visible_elements(MainPageLocators.MODAL_OVERLAY)
        return self

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

    def close_modal(self):
        self.close_visible_modal(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_invisible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def ingredient_counter(self, card_locator):
        card = self.visible(card_locator)
        return int(card.find_element(*MainPageLocators.INGREDIENT_COUNTER).text)

    @allure.step("Добавить ингредиент и дождаться увеличения счётчика")
    def add_ingredient(self, card_locator):
        before = self.ingredient_counter(card_locator)
        self.drag_and_drop(card_locator, MainPageLocators.BASKET)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda _: self.ingredient_counter(card_locator) > before
            )
        except TimeoutException:
            self.html5_drag_and_drop(card_locator, MainPageLocators.BASKET)
            WebDriverWait(self.driver, ORDER_TIMEOUT).until(
                lambda _: self.ingredient_counter(card_locator) > before
            )
        return self.ingredient_counter(card_locator)

    @allure.step("Собрать бургер")
    def assemble_burger(self):
        self.add_ingredient(MainPageLocators.BUN_CARD)
        self.add_ingredient(MainPageLocators.FILLING_CARD)

    @allure.step("Оформить заказ")
    def create_order(self):
        def real_order_number(driver):
            elements = driver.find_elements(*MainPageLocators.ORDER_NUMBER)
            for element in elements:
                text = element.text.strip()
                if element.is_displayed() and text.isdigit() and text != "9999":
                    return int(text)
            return False

        last_error = None
        for attempt in range(2):
            with allure.step(f"Попытка оформления заказа №{attempt + 1}"):
                self.click(MainPageLocators.ORDER_BUTTON)
                try:
                    return WebDriverWait(
                        self.driver, ORDER_ATTEMPT_TIMEOUT
                    ).until(real_order_number)
                except TimeoutException as error:
                    last_error = error
                    self.close_visible_modal(MainPageLocators.MODAL_CLOSE_BUTTON)
                    self.wait_no_visible_elements(MainPageLocators.ORDER_NUMBER)

        raise last_error

    @allure.step("Закрыть окно оформленного заказа")
    def close_order_modal(self):
        self.close_visible_modal(MainPageLocators.MODAL_CLOSE_BUTTON)
        WebDriverWait(self.driver, ORDER_TIMEOUT).until(
            lambda driver: not any(
                element.is_displayed()
                for element in driver.find_elements(*MainPageLocators.ORDER_NUMBER)
            )
        )
