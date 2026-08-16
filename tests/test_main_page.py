import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers UI")
@allure.feature("Основная функциональность")
class TestMainPage:
    @allure.title("Переход в конструктор по ссылке в шапке")
    def test_constructor_link_opens_main_page(self, driver):
        FeedPage(driver).open()
        main_page = MainPage(driver)

        main_page.click_constructor()

        assert main_page.is_opened()

    @allure.title("Переход в ленту заказов по ссылке в шапке")
    def test_feed_link_opens_order_feed(self, driver):
        main_page = MainPage(driver).open()
        feed_page = FeedPage(driver)

        main_page.click_feed()

        assert feed_page.is_opened()

    @allure.title("Клик по ингредиенту открывает окно с деталями")
    def test_ingredient_click_opens_details_modal(self, driver):
        main_page = MainPage(driver).open()

        main_page.open_ingredient_details()

        assert main_page.ingredient_modal_is_open()

    @allure.title("Окно с деталями закрывается по крестику")
    def test_ingredient_modal_closes_by_cross(self, driver):
        main_page = MainPage(driver).open()
        main_page.open_ingredient_details()

        main_page.close_modal()

        assert main_page.ingredient_modal_is_closed()

    @allure.title("При добавлении ингредиента его счётчик увеличивается")
    def test_ingredient_counter_increases_after_drag(self, driver):
        main_page = MainPage(driver).open()
        before = main_page.sauce_counter()

        after = main_page.add_sauce()

        assert after > before
