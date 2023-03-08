import allure
from src.core.BrowserTools import BrowserTools, HelperWebElementsMixin
from src.pages.page_user.locators import UserPageLocators as Locators

from src.assertions.assertions import check_that_data_is_equal


class UserPage(BrowserTools, HelperWebElementsMixin):
    def write_email(self, email: str):
        with allure.step(f"Ввести почту: {email}"):
            self.find_element_send_key(Locators.INPUT_EMAIL, email)

    def write_lastname(self, lastname: str):
        with allure.step(f"Ввести фамилию: {lastname}"):
            self.find_element_send_key(Locators.INPUT_LAST_NAME, lastname)

    def write_firstname(self, firstname: str):
        with allure.step(f"Ввести имя: {firstname}"):
            self.find_element_send_key(Locators.INPUT_FIRST_NAME, firstname)

    def write_middlename(self, middlename: str):
        with allure.step(f"Ввести отчество: {middlename}"):
            self.find_element_send_key(Locators.INPUT_MIDDLE_NAME, middlename)

    def write_password(self, pwd: str):
        with allure.step(f"Ввести пароль: {pwd}"):
            self.find_element_send_key(Locators.INPUT_PWD, pwd)

    def write_rpt_pwd(self, rpt_pwd: str):
        with allure.step(f"Ввести повторно пароль: {rpt_pwd}"):
            self.find_element_send_key(Locators.INPUT_PWD, rpt_pwd)

    def click_button_save_changes(self):
        with allure.step("Нажать на кнопку Сохранить"):
            self.find_element_click_action(Locators.BTN_SAVE, scroll_to_el=True)

    def check_lastname(self, lastname: str):
        with allure.step("Проверка, что поле фамилия изменилось"):
            element = self.get_element_located(Locators.INPUT_LAST_NAME)
            value_field = self.get_attribute_value_element(element)
            check_that_data_is_equal(lastname, value_field)

    def check_firstname(self, firstname: str):
        with allure.step("Проверка, что поле имя изменилось"):
            element = self.get_element_located(Locators.INPUT_FIRST_NAME)
            value_field = self.get_attribute_value_element(element)
            check_that_data_is_equal(firstname, value_field)

    def check_middlename(self, middlename: str):
        with allure.step("Проверка, что поле отчество изменилось"):
            element = self.get_element_located(Locators.INPUT_MIDDLE_NAME)
            value_field = self.get_attribute_value_element(element)
            check_that_data_is_equal(middlename, value_field)
