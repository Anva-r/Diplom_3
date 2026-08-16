import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from constants import DEFAULT_TIMEOUT, REGISTER_URL, USER_URL
from helpers import generate_user_data


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=("all", "chrome", "firefox"),
        help="Браузер для запуска: all, chrome или firefox",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Запустить браузеры с интерфейсом",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(params=("chrome", "firefox"))
def driver(request):
    browser_name = request.param
    selected_browser = request.config.getoption("--browser")
    if selected_browser != "all" and selected_browser != browser_name:
        pytest.skip(f"Выбран браузер {selected_browser}")

    headed = request.config.getoption("--headed")
    if browser_name == "chrome":
        options = ChromeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        if not headed:
            options.add_argument("-headless")
        options.add_argument("--width=1440")
        options.add_argument("--height=1000")
        browser = webdriver.Firefox(options=options)

    browser.set_page_load_timeout(DEFAULT_TIMEOUT)
    allure.dynamic.parameter("browser", browser_name)
    yield browser

    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        allure.attach(
            browser.get_screenshot_as_png(),
            name=f"failure-{browser_name}",
            attachment_type=allure.attachment_type.PNG,
        )
    browser.quit()


@pytest.fixture
def registered_user():
    user_data = generate_user_data()
    response = requests.post(REGISTER_URL, json=user_data, timeout=DEFAULT_TIMEOUT)
    if response.status_code != 200:
        pytest.fail(
            f"Не удалось создать UI-пользователя: "
            f"{response.status_code} {response.text}"
        )
    user = {**user_data, **response.json()}

    yield user

    access_token = user.get("accessToken")
    if access_token:
        requests.delete(
            USER_URL,
            headers={"Authorization": access_token},
            timeout=DEFAULT_TIMEOUT,
        )
