import allure

from constants import BASE_URL
from locators import FeedPageLocators, MainPageLocators
from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers UI")
@allure.feature("Основная функциональность")
class TestMainPage:
    @allure.title("Переход в конструктор по ссылке в шапке")
    def test_constructor_link_opens_main_page(self, driver):
        FeedPage(driver).open()

        MainPage(driver).click_constructor()

        assert driver.current_url == f"{BASE_URL}/"
        assert MainPage(driver).is_visible(MainPageLocators.PAGE_TITLE)

    @allure.title("Переход в ленту заказов по ссылке в шапке")
    def test_feed_link_opens_order_feed(self, driver):
        main_page = MainPage(driver).open()

        main_page.click_feed()

        assert driver.current_url == f"{BASE_URL}/feed"
        assert FeedPage(driver).is_visible(FeedPageLocators.PAGE_TITLE)

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

        assert not main_page.ingredient_modal_is_open()

    @allure.title("При добавлении ингредиента его счётчик увеличивается")
    def test_ingredient_counter_increases_after_drag(self, driver):
        main_page = MainPage(driver).open()
        before = main_page.ingredient_counter(MainPageLocators.SAUCE_CARD)

        after = main_page.add_ingredient(MainPageLocators.SAUCE_CARD)

        assert after > before
