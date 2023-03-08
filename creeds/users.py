from dataclasses import dataclass

from decouple import config
from schemas import User


class Users:

    @dataclass
    class User_1:
        email: [str] = "example@email.com"
        password: [str] = "password"
        last_name: [str] = 'Фамилия'
        first_name: [str] = 'Имя'
        middle_name: str = 'Отчество'

    @dataclass
    class User_2:
        email: str = "example2@email.com"
        password: str = "password1"
        last_name: str = 'Фамилия1'
        first_name: str = 'Имя1'
        middle_name: str = 'Отчество1'
