import allure
from selenium.webdriver.support.ui import WebDriverWait

from constants import BASE_URL, ORDER_TIMEOUT
from locators import FeedPageLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    URL = f"{BASE_URL}/feed"

    @allure.step("Открыть ленту заказов")
    def open(self):
        self.open_url(self.URL)
        self.visible(FeedPageLocators.PAGE_TITLE)
        self.visible(FeedPageLocators.TOTAL_COUNTER)
        return self

    def total_counter(self):
        return int(self.text(FeedPageLocators.TOTAL_COUNTER).replace(" ", ""))

    def today_counter(self):
        return int(self.text(FeedPageLocators.TODAY_COUNTER).replace(" ", ""))

    @allure.step("Дождаться увеличения счётчика за всё время")
    def wait_total_counter_greater_than(self, previous_value):
        return WebDriverWait(self.driver, ORDER_TIMEOUT).until(
            lambda _: (
                current
                if (current := self.total_counter()) > previous_value
                else False
            )
        )

    @allure.step("Дождаться увеличения счётчика за сегодня")
    def wait_today_counter_greater_than(self, previous_value):
        return WebDriverWait(self.driver, ORDER_TIMEOUT).until(
            lambda _: (
                current
                if (current := self.today_counter()) > previous_value
                else False
            )
        )

    @allure.step("Дождаться номера заказа в разделе «В работе»")
    def wait_order_in_progress(self, order_number):
        expected = str(order_number).zfill(7)

        def order_is_visible(_):
            text = self.visible(FeedPageLocators.IN_PROGRESS_LIST).text
            return expected in text or str(order_number) in text.split()

        return WebDriverWait(self.driver, ORDER_TIMEOUT).until(order_is_visible)
