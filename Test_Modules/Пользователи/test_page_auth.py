import pytest
import allure

from conftest import catch_exception
from creeds import Users
from src.pages.page_authorization.authorization_page import AuthorizationPage
from src.utils.helper import allure_collect_decorator


@allure.epic("Пользователи")
@pytest.mark.user
class TestUser:

    @allure_collect_decorator(
        title='Авторизация',
        description_case='Пользователи может авторизоваться',
        severity_allure=allure.severity_level.CRITICAL,
        allure_story="Страница авторизации"
    )
    @pytest.mark.smoke
    @pytest.mark.regress
    @catch_exception
    @pytest.mark.parametrize("type_user, user_data", [
        ("admin", Users.User_1),
        ('user_simple', Users.User_2)
    ])
    def test_user_can_auth_ID_USER_301(self,
                                       type_user, user_data,
                                       get_base_host,
                                       browser,
                                       ):
        # ARRAY
        auth_page = AuthorizationPage(browser)
        auth_page.open_new_window(get_base_host)

        # ACT
        auth_page.auth_user(user_data, type_user)

        # ASSERT
        auth_page.wait(2)
        auth_page.check_user_can_see_dash_board_page()

    @allure_collect_decorator(
        title='Неверные данные при авторизации',
        description_case='Пользователи видит сообщение введении неверных данных при попытке авторизоваться',
        severity_allure=allure.severity_level.NORMAL,
        allure_story="Страница авторизации"
    )
    @pytest.mark.smoke
    @pytest.mark.regress
    @catch_exception
    def test_user_can_see_error_msg_ID_USER_302(self, browser, get_base_host):
        # Array
        user = Users.User_2
        not_correct_pwd = "not_correct_pwd"
        error_msg = "Неправильный логин или пароль"

        # Act
        auth_page = AuthorizationPage(browser)
        auth_page.open_new_window(get_base_host)
        auth_page.write_email(user.email)
        auth_page.write_password(not_correct_pwd)
        auth_page.click_btn_login()

        # Assert
        auth_page.check_user_can_see_error_msg(error_msg)

    @allure_collect_decorator(
        title='Видимость пароля при авторизации',
        description_case='Пользователи может увидеть пароль после нажатия на глазок ',
        severity_allure=allure.severity_level.MINOR,
        allure_story="Страница авторизации"
    )
    @pytest.mark.regress
    @catch_exception
    def test_user_can_see_pwd_ID_USER_303(self, browser, get_base_host):
        # Array
        user = Users.User_2

        # Act
        auth_page = AuthorizationPage(browser)
        auth_page.open_new_window(get_base_host)
        auth_page.write_email(user.email)
        auth_page.write_password(user.password)
        auth_page.click_btn_show_pwd()

        # Assert
        auth_page.check_that_user_can_see_password()

        # Act
        auth_page.click_btn_show_pwd()

        # Assert
        auth_page.check_that_user_cannot_see_password()

    @allure_collect_decorator(
        title='Сброс пароля',
        description_case='Пользователи может сбросить пароль',
        severity_allure=allure.severity_level.CRITICAL,
        allure_story="Страница авторизации"
    )
    @pytest.mark.smoke
    @pytest.mark.regress
    @catch_exception
    def test_user_can_reset_pwd_ID_USER_304(self, browser, get_base_host):
        # Array
        user = Users.User_2
        msg = "На вашу почту было выслано письмо c инструкцией"

        # Act
        auth_page = AuthorizationPage(browser)
        auth_page.open_new_window(get_base_host)
        auth_page.click_forgot_pwd()

        # Assert
        auth_page.check_user_see_forget_page()

        # Act
        auth_page.write_email_form_forgot_pwd(user.email)
        auth_page.click_btn_send_letter_for_reset_pwd()

        # Assert
        auth_page.check_user_can_see_success_msg_send_letter(msg)

    @allure_collect_decorator(
        title='Сообщение при сбросе пароля об некорректной почте',
        description_case='Пользователи видит сообщение о неверной почте при сбросе пароля',
        severity_allure=allure.severity_level.CRITICAL,
        allure_story="Страница авторизации"
    )
    @pytest.mark.regress
    @catch_exception
    def test_user_can_reset_pwd_ID_USER_305(self, browser, get_base_host):
        # Array
        user = Users.User_2
        msg = "На вашу почту было выслано письмо c инструкцией"

        # Act
        auth_page = AuthorizationPage(browser)
        auth_page.open_new_window(get_base_host)
        auth_page.click_forgot_pwd()

        # Assert
        auth_page.check_user_see_forget_page()

        # Act
        auth_page.write_email_form_forgot_pwd(user.email)
        auth_page.click_btn_send_letter_for_reset_pwd()

        # Assert
        auth_page.check_user_can_see_success_msg_send_letter(msg)

    @allure_collect_decorator(
        title='Сообщение при сбросе пароля об некорректной почте',
        description_case='Пользователи видит сообщение о неверной почте при сбросе пароля',
        severity_allure=allure.severity_level.CRITICAL,
        allure_story="Страница авторизации"
    )
    @pytest.mark.regress
    @catch_exception
    def test_user_can_reset_pwd_ID_USER_306(self, browser, get_base_host):
        # Array
        email = "notcreatedemail@test.su"
        msg = "Пользователя с таким email не существует"

        # Act
        auth_page = AuthorizationPage(browser)
        auth_page.open_new_window(get_base_host)
        auth_page.click_forgot_pwd()

        # Assert
        auth_page.check_user_see_forget_page()

        # Act
        auth_page.write_email_form_forgot_pwd(email)
        auth_page.click_btn_send_letter_for_reset_pwd()

        # Assert
        auth_page.check_user_can_see_error_msg(msg)