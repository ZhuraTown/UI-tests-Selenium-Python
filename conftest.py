import pytest
import functools
from decouple import config
from selenium import webdriver
from allure import attachment_type, attach
from selenium.common.exceptions import \
    TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException

from src.core.driver import DriverBrowser
from fixtures import *


browser: webdriver


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="g",
                     help='Браузер для запуска тестов')
    parser.addoption('--headless', action='store_true', default=None,
                     help='Запуск браузера без окна')
    parser.addoption('--host_name', action='store', default=config("HOST"),
                     help='Выберите хост, для работы тестов')
    parser.addoption('--remote_browser', action='store_true', default=None,
                     help='Запуск тестов через удаленный сервер')


@pytest.fixture(scope='session')
def browser_setup(request):
    global browser
    browser_name = request.config.getoption('--browser_name')
    remote_browser = request.config.getoption('--remote_browser')
    browser_headless = request.config.getoption('--headless')
    mk_video = request.config.getoption('--mk_video')
    host = request.config.getoption('--host_name')
    executor = request.config.getoption('--executor')
    browser = DriverBrowser(browser_name=browser_name,
                            browser_headless=browser_headless,
                            remote_browser=remote_browser,
                            mk_video=mk_video,
                            executor=executor).setup_driver()
    try:
        browser.get(host)
        yield browser
    finally:
        browser.quit()


@pytest.fixture()
def get_base_host(request):
    return request.config.getoption("--host_name")


@pytest.fixture()
def browser(browser_setup):
    # SetUp browser
    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear();")
    yield browser


def catch_exception(func):
    """
    Функция ловит любые падение и делает скриншот, который затем добавляет к отчету
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            attach(browser.get_screenshot_as_png(), name='Screen', attachment_type=attachment_type.PNG)
            raise
    return wrapper


def check_element(func):
    def wrapper(*args, **kwargs):
        find_element = args[1]
        try:
            result = func(*args, **kwargs)
            return result
        except TimeoutException:
            raise TimeoutException(f"Элемента нету на странице.\n"
                                   f"Метод: [{find_element[0]}]\n"
                                   f"Локатор: [{find_element[1]}]")
        except ElementClickInterceptedException:
            raise ElementClickInterceptedException(f"Элемент не в зоне видимости пользователя или перекрыт.\n"
                                                   f"Метод: [{find_element[0]}]\n"
                                                   f"Локатор: [{find_element[1]}]")
        except StaleElementReferenceException:
            raise StaleElementReferenceException(f"Элемент был в зоне видимости, но затем исчез из DOM.\n"
                                                 f"Метод: [{find_element[0]}]\n"
                                                 f"Локатор: [{find_element[1]}]")
        except ElementNotInteractableException:
            raise ElementNotInteractableException(f"С элементом не удается взаимодействовать\n"
                                                  f"Метод: [{find_element[0]}]\n"
                                                  f"Локатор: [{find_element[1]}]")

    return wrapper
