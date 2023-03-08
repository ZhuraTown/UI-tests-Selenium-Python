import requests
from http import HTTPStatus

from schemas import User
from src.utils.api_modules import BaseApiClass


class UserModule(BaseApiClass):
    """
    Модуль Пользователи
    """
    URL_USER = "/users"

    def find_user(self, name: str) -> [User] or []:
        """
        Поиск пользователя с именем
        """
        self.authorization()
        r = requests.get(
            url=self.host + self.URL_USER,
            headers={'Authorization': f'Bearer {self.access_token}'},
            params={
                "search": name
            })

        if r.status_code == HTTPStatus.OK:
            r = r.json()
            users = []
            for user in r:
                users.append(User.parse_obj(user))
            return users
        self.raise_exception_if_received_not_expected_status_code(r)

    def generate_sesame(self, email: str) -> str:
        url = f"{self.URL_USER}/register_user"
        r = requests.post(
            url=self.host + url,
            json={'email': email},
            headers={'Authorization': f'Bearer {self.access_token}'})
        if r.status_code == HTTPStatus.OK:
            r = r.json()
            return r['sesame']
        self.raise_exception_if_received_not_expected_status_code(r)

    def register_user(self, sesame: str, user: User) -> User:
        """
        Регистрация пользователя
        """
        url = f"{self.URL_USER}/register_user"
        r = requests.put(
            url=self.host + url,
            params={'sesame': sesame},
            json={user.dict()})

        if r.status_code == HTTPStatus.OK:
            r = r.json()
            return User.parse_obj(r)
        self.raise_exception_if_received_not_expected_status_code(r)

    def delete_user(self, user_id: int):
        self.authorization()
        url = f"{self.URL_USER}/{user_id}"

        requests.delete(
            url=self.host + url,
            headers={'Authorization': f'Bearer {self.access_token}'},
        )

    def get_me(self) -> User:
        self.authorization()
        url = f"{self.URL_USER}/me"
        r = requests.get(
            url=self.host + url,
            headers={'Authorization': f'Bearer {self.access_token}'})

        if r.status_code == HTTPStatus.OK:
            r = r.json()
            user = User.parse_obj(r)
            return user
        self.raise_exception_if_received_not_expected_status_code(r)

