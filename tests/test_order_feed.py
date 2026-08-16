import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers UI")
@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Новый заказ увеличивает счётчик за всё время")
    def test_new_order_increases_total_counter(self, driver, registered_user):
        feed_page = FeedPage(driver).open()
        before = feed_page.total_counter()

        MainPage(driver).create_order_for_user(
            registered_user["email"], registered_user["password"]
        )
        feed_page.open()
        after = feed_page.wait_total_counter_greater_than(before)

        assert after > before

    @allure.title("Новый заказ увеличивает счётчик за сегодня")
    def test_new_order_increases_today_counter(self, driver, registered_user):
        feed_page = FeedPage(driver).open()
        before = feed_page.today_counter()

        MainPage(driver).create_order_for_user(
            registered_user["email"], registered_user["password"]
        )
        feed_page.open()
        after = feed_page.wait_today_counter_greater_than(before)

        assert after > before

    @allure.title("Номер нового заказа появляется в разделе «В работе»")
    def test_new_order_number_appears_in_progress(self, driver, registered_user):
        order_number = MainPage(driver).create_order_for_user(
            registered_user["email"], registered_user["password"]
        )

        feed_page = FeedPage(driver).open()

        assert feed_page.wait_order_in_progress(order_number)
