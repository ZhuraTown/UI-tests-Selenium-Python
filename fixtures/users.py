import pytest

from creeds import Users
from schemas import User
from src.utils.api_interface import ApiExampleInterface
from src.utils.generators import generate_user


@pytest.fixture(scope='session')
def register_user():
    user_login = Users.User_1
    user_register = User.parse_obj(Users.User_2().__dict__)
    Api = ApiExampleInterface(user_login.email, user_login.password)
    sesame = Api.generate_sesame(user_register.email)
    user = Api.register_user(sesame, user_register)
    return user


@pytest.fixture()
def generate_user_data():
    user = generate_user()
    return user
