import pytest
from creeds import Users
from conftest import catch_exception
from src.assertions.assertions import *
from src.utils.helper import allure_collect_decorator
from src.pages.page_authorization.authorization_page import AuthorizationPage
from src.pages.page_user.user_page import UserPage


@allure.epic("Пользователи")
@allure.feature('Настройка профиля пользователя')
@pytest.mark.user
class TestUserData:

    @allure_collect_decorator(
        title='Изменение ФИО',
        description_case='Пользователь может изменить ФИО',
        severity_allure=allure.severity_level.NORMAL,
        allure_story="Данные пользователя"
    )
    @pytest.mark.smoke
    @pytest.mark.regress
    @catch_exception
    def test_user_can_change_FIO_ID_USER_201(self,
                                             browser, get_base_host, generate_user_data):
        # ARRAY
        user_data = generate_user_data
        user, type_user = Users.User_2, "user"
        AuthorizationPage(browser).auth_user(user, type_user)

        # ACT
        user_page = UserPage(browser)
        user_page.write_lastname(user_data.last_name)
        user_page.write_firstname(user_data.first_name)
        user_page.write_middlename(user_data.middle_name)
        user_page.click_button_save_changes()

        # ASSERT
        user_page.check_lastname(user_data.last_name)
        user_page.check_firstname(user_data.first_name)
        user_page.check_middlename(user_data.middle_name)
