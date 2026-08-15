import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait

from constants import DEFAULT_TIMEOUT


class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу {url}")
    def open_url(self, url):
        self.driver.get(url)

    def visible(self, locator):
        return self.wait.until(conditions.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(conditions.element_to_be_clickable(locator))

    @allure.step("Нажать на элемент")
    def click(self, locator):
        self.clickable(locator).click()

    @allure.step("Заполнить поле")
    def fill(self, locator, value):
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator):
        return self.visible(locator).text

    def is_visible(self, locator):
        try:
            self.visible(locator)
            return True
        except TimeoutException:
            return False

    def wait_invisible(self, locator):
        return self.wait.until(conditions.invisibility_of_element_located(locator))

    def wait_no_visible_elements(self, locator):
        return self.wait.until(
            lambda driver: not any(
                element.is_displayed() for element in driver.find_elements(*locator)
            )
        )

    @allure.step("Закрыть видимое модальное окно")
    def close_visible_modal(self, locator):
        def visible_button(driver):
            visible_buttons = [
                element
                for element in driver.find_elements(*locator)
                if element.is_displayed() and element.is_enabled()
            ]
            # React оставляет в DOM несколько экземпляров modal portal.
            # Последний видимый элемент принадлежит верхнему окну.
            return visible_buttons[-1] if visible_buttons else False

        self.wait.until(visible_button).click()

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.visible(source_locator)
        target = self.visible(target_locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", source
        )
        ActionChains(self.driver).click_and_hold(source).pause(0.3).move_to_element(
            target
        ).pause(0.5).release().perform()

    @allure.step("Повторить перетаскивание через HTML5-события")
    def html5_drag_and_drop(self, source_locator, target_locator):
        source = self.visible(source_locator)
        target = self.visible(target_locator)
        script = """
            const source = arguments[0];
            const target = arguments[1];
            const transfer = new DataTransfer();
            transfer.setData('text/plain', 'stellar-burgers-ingredient');
            const fire = (element, type) => element.dispatchEvent(
                new DragEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: transfer
                })
            );
            fire(source, 'dragstart');
            fire(target, 'dragenter');
            fire(target, 'dragover');
            fire(target, 'drop');
            fire(source, 'dragend');
        """
        self.driver.execute_script(script, source, target)

    def wait_url(self, expected_url):
        self.wait.until(conditions.url_to_be(expected_url))

    @property
    def current_url(self):
        return self.driver.current_url
