import logging

from decouple import config
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, JavascriptException

from conftest import check_element


class SettingBrowserTools:
    TIMEOUT_WAIT_ELEMENT = config("TIMEOUT_WAIT_ELEMENT")
    TIMEOUT_WAIT_IMPLICITLY = 1
    TIMEOUT_WAIT_ELEMENT_FOR_SCROLLER = config("TIMEOUT_WAIT_ELEMENT_FOR_SCROLLER")


class ElementScroller:
    SCROLL_TO_LOCATOR_XPATH = "(document.evaluate(\"{}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).scrollIntoView(true)"
    SCROLL_TO_LOCATOR_CSS = "document.querySelector('{}').scrollIntoView(false)"
    SCROLL_TO_LOCATOR_ID = "document.querySelector('#{}').scrollIntoView(false)"

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.driver.implicitly_wait(SettingBrowserTools.TIMEOUT_WAIT_IMPLICITLY)

    @check_element
    def scroll_to_element(self, find_element: tuple,
                          delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT_FOR_SCROLLER):
        method = find_element[0]
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(find_element))
            if method in "xpath":
                self.driver.execute_script(str(self.SCROLL_TO_LOCATOR_XPATH.format(find_element[1])))
            elif method in "id":
                self.driver.execute_script(str(self.SCROLL_TO_LOCATOR_ID.format(find_element[1])))
            elif method in "css selector":
                self.driver.execute_script(str(self.SCROLL_TO_LOCATOR_CSS.format(find_element[1])))
        except JavascriptException:
            logging.info(
                f"Не удалось проскролить до элемента:\n"f"method: {find_element[0]}\n"f"locator: {find_element[1]}")


class Browser:

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.driver.implicitly_wait(SettingBrowserTools.TIMEOUT_WAIT_IMPLICITLY)

    def open_new_window(self, url):
        self.driver.get(url)

    def refresh_current_page(self):
        self.driver.refresh()

    def get_current_url(self):
        return self.driver.execute_script("return (()=> { return window.location.href})()")

    def switch_to_next_window(self):
        last_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(last_window)

    def switch_frame(self, frame: WebElement = None):
        """
        Переключить фрейм
        """
        if frame:
            self.driver.switch_to.frame(frame)
            return
        self.driver.switch_to.default_content()

    @check_element
    def switch_frame_with_element(self, find_element):
        """
        Переключить фрейм
        """
        WebDriverWait(self.driver, SettingBrowserTools.TIMEOUT_WAIT_ELEMENT).until(EC.frame_to_be_available_and_switch_to_it(find_element))


class SimulatorMouse:

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.driver.implicitly_wait(SettingBrowserTools.TIMEOUT_WAIT_IMPLICITLY)

    @check_element
    def find_element_click_action(self, find_element,
                                  delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT,
                                  scroll_to_el: bool = False,
                                  duration: int = 600):
        if scroll_to_el:
            ElementScroller(self.driver).scroll_to_element(find_element)

        element = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(find_element))
        ActionChains(self.driver, duration=duration).move_to_element(element).click(element).pause(0.1).perform()

    @check_element
    def drag_and_drop_elements(self, element_1: WebElement, element_2: WebElement, duration: int = 1500):
        """
        Переместить element_1 на место element_2
        duration: время выполнения действий
        element_1: WebElement(найденный) который будет переносится
        element_2: WebElement(найденный) куда будет переносится
        """
        action = ActionChains(self.driver, duration=duration)
        action.move_to_element(element_1).click().click_and_hold()
        action.move_to_element(element_2).pause(1)
        action.release()
        action.perform()


class ElementWaitFinder:

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.driver.implicitly_wait(SettingBrowserTools.TIMEOUT_WAIT_IMPLICITLY)

    @check_element
    def element_is_visible(self, find_element, delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT):
        try:
            WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located(find_element))
            return True
        except (TimeoutException, TimeoutError):
            return False

    @check_element
    def element_is_located(self, find_element, delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT):
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(find_element))
            return True
        except (TimeoutException, TimeoutError):
            return False

    @check_element
    def element_is_not_clickable(self, find_element, delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT):
        return WebDriverWait(self.driver, delay).until_not(EC.element_to_be_clickable(find_element))

    @check_element
    def get_element_located(self, find_element, delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT) -> WebElement:
        return WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(find_element))

    @check_element
    def find_element_send_key(self, find_element: tuple, text: str, scroll_to_el: bool = False,
                              delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT):
        if scroll_to_el:
            ElementScroller(self.driver).scroll_to_element(find_element)

        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(find_element)).send_keys(text)

    @check_element
    def find_element_click(self, find_element, scroll_to_el: bool = False,
                           delay: int = SettingBrowserTools.TIMEOUT_WAIT_ELEMENT):
        if scroll_to_el:
            ElementScroller(self.driver).scroll_to_element(find_element)
        WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable(find_element)).click()


class HelperWebElementsMixin:

    def _is_correct(self, element: any):
        if not isinstance(element, WebElement):
            raise ValueError(f'Expected class WebElement, received: {type(element).__name__}')

    def get_attribute_value_element(self, element_page: WebElement):
        self._is_correct(element_page)
        return element_page.get_attribute('value')

    def get_attribute_type_element(self, element_page: WebElement):
        self._is_correct(element_page)
        return element_page.get_attribute('type')

    def get_attribute_text_element(self, element_page: WebElement):
        self._is_correct(element_page)
        return element_page.text

    def element_is_displayed(self, element_page: WebElement) -> bool:
        self._is_correct(element_page)
        return element_page.is_displayed()

    def clear_input(self, element_page: WebElement):
        self._is_correct(element_page)
        element_page.clear()


class GeneratorDynamicLocators:

    @staticmethod
    def div_and_collect_locator(locator: tuple, *args
                                ) -> tuple:
        """
        Метод разделяет вошедший кортеж и форматирует строку
        Например на ВХОД: (By.XPATH, "//div[contains(@class, {})]"), "base-class"
        ВЫХОД: (By.XPATH, "//div[contains(@class, base-class)]")
        """
        method, locator = locator
        locator = locator.format(*args)
        return method, locator


class BrowserTools(Browser, GeneratorDynamicLocators, ElementWaitFinder, SimulatorMouse, JSClicker, ElementScroller):
    """
    """
