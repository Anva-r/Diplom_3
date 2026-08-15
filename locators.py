from selenium.webdriver.common.by import By

from constants import BUN_ID, FILLING_ID, SAUCE_ID


class HeaderLocators:
    CONSTRUCTOR_LINK = (
        By.XPATH,
        "//a[@href='/' and .//p[normalize-space()='Конструктор']]",
    )
    FEED_LINK = (
        By.XPATH,
        "//a[@href='/feed' and .//p[normalize-space()='Лента Заказов']]",
    )


class MainPageLocators:
    PAGE_TITLE = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")
    BUN_CARD = (By.CSS_SELECTOR, f"a[href='/ingredient/{BUN_ID}']")
    FILLING_CARD = (By.CSS_SELECTOR, f"a[href='/ingredient/{FILLING_ID}']")
    SAUCE_CARD = (By.CSS_SELECTOR, f"a[href='/ingredient/{SAUCE_ID}']")
    BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket__']")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "div[class*='counter_counter__'] p")
    INGREDIENT_MODAL_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Детали ингредиента']",
    )
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay__']")
    ORDER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Оформить заказ']",
    )
    ORDER_NUMBER = (
        By.XPATH,
        "//p[normalize-space()='идентификатор заказа']/preceding-sibling::h2[1]",
    )


class LoginPageLocators:
    PAGE_TITLE = (By.XPATH, "//h2[normalize-space()='Вход']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")


class FeedPageLocators:
    PAGE_TITLE = (By.XPATH, "//h1[normalize-space()='Лента заказов']")
    TOTAL_COUNTER = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за все время:']/following-sibling::p",
    )
    TODAY_COUNTER = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p",
    )
    IN_PROGRESS_LIST = (
        By.CSS_SELECTOR,
        "ul[class*='OrderFeed_orderListReady__']",
    )
