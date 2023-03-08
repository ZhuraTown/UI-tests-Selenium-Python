import requests

from http import HTTPStatus
from decouple import config


class BaseApiClass:

    def __init__(self, login: str, password: str):

        self.login = login
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.host = config('HOST') + "/api"

    def authorization(self):
        url_auth = '/accounts/auth'
        creds = {
            'email': f'{self.login}',
            'password': f'{self.password}'
        }

        if not self.access_token:
            response = requests.post(
                url=self.host + url_auth,
                json=creds
            )
            if response.status_code == HTTPStatus.OK:
                r = response.json()
                self.access_token = r['access']
                self.refresh_token = r['refresh']
                return
            self.raise_exception_if_received_not_expected_status_code(response)

    @staticmethod
    def raise_exception_if_received_not_expected_status_code(response: requests):
        a = (f"Не получил ожидаемый ответ сервера. \n"
             f"Адрес: {response.url}\n"
             f"Код сервера: {response.status_code}\n"
             f"Получен ответ:\n {response.text[:2000]}")
        raise Exception(a)

    def get_access_token(self):
        return self.access_token

    def get_refresh_token(self):
        return self.refresh_token

    def get_host(self):
        return self.host
