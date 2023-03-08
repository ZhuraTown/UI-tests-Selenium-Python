import allure

from src.assertions.assertions import check_that_data_present_in_received
from src.core.BrowserTools import HelperWebElementsMixin, BrowserTools
from src.pages.page_authorization.locators import AuthorizationPageLocators as Locators


class AuthorizationPage(BrowserTools, HelperWebElementsMixin):

    def write_email(self, email: str):
        with allure.step(f"Ввести в поле Email: {email}"):
            self.find_element_send_key(Locators.INPUT_EMAIL, email)

    def write_password(self, password: str):
        with allure.step(f"Ввести в поле пароль: {password}"):
            self.find_element_send_key(Locators.INPUT_PWD, password)

    def write_email_form_forgot_pwd(self, email: str):
        with allure.step(f"Ввести почту({email}) для сброса пароля"):
            self.find_element_send_key(Locators.INPUT_EMAIL, email)

    def click_btn_login(self):
        with allure.step("Нажать на кнопку Войти"):
            self.find_element_click(Locators.BTN_LOGIN)

    def click_forgot_pwd(self):
        with allure.step("Нажать на 'Забыли пароль?'"):
            self.find_element_click(Locators.BTN_FORGOT_PWD)

    def auth_user(self, user, type_user: str):
        with allure.step(f"Авторизоваться типом пользователя: {type_user}"):
            self.write_email(user.email)
            self.write_password(user.password)
            self.click_btn_login()

    def catch_error_msg(self):
        error_msg = self.get_element_located(Locators.ERR_MSG)
        return self.get_attribute_text_element(error_msg)

    def check_user_can_see_error_msg(self, msg: str):
        with allure.step("Проверка, что пользователь видит сообщение с ошибкой"):
            with allure.step(f"Сообщение: {msg}"):
                current_msg = self.catch_error_msg()
                check_that_data_present_in_received(msg, current_msg)