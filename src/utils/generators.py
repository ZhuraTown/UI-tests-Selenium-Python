import random
import string
import datetime
import calendar
from faker import Faker

from schemas import User


def generate_random_string(length=10):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def generate_random_mobile_number():
    first_numbers = str(random.randint(900, 999))
    second_numbers = str(random.randint(1, 999)).zfill(3)
    third_numbers = str(random.randint(1, 99)).zfill(2)
    fourth_numbers = '00'
    return "+7(" + first_numbers + ")" + second_numbers + "-" + third_numbers + "-" + fourth_numbers


def generate_random_phone_number():
    first_numbers = str(random.randint(900, 999))
    second_numbers = str(random.randint(1, 999)).zfill(3)
    third_numbers = str(random.randint(1, 99)).zfill(2)
    return f"7{first_numbers}{second_numbers}{third_numbers}00"


def generate_random_number_between_1_and_this_number(number):
    return random.randint(1, number)


def generate_random_email_with_random_dom():
    return generate_random_string(3) + str(generate_random_number_between_1_and_this_number(9)) \
           + generate_random_string(2) + "@" + generate_random_string(3) + str(
        generate_random_number_between_1_and_this_number(9)) \
           + "." + generate_random_string(3)


def generate_user() -> User:
    f = Faker('ru_RU')
    name = f.name().split(' ')
    email = generate_random_email_with_random_dom()
    pwd = "examplepassword"
    user = User(
        last_name=name[0],
        first_name=name[1],
        middle_name=name[2],
        email=email,
        password=pwd
    )
    return user


def generate_location() -> str:
    return Faker("ru_RU").city_name()


def generate_date_now_plus_one_day():
    date_tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    return date_tomorrow.date().strftime('%d.%m.%Y')


def generate_date_today_str():
    """
    Получить сегодняшнюю дату в формате datetime
    """
    return datetime.datetime.now().strftime('%d%m%Y')


def generate_date_today_with_form(form: str):
    return datetime.datetime.now().strftime(form)


def generate_date_today_timedelta_days_form(timedelta: int, form: str):
    if timedelta < 0:
        return (datetime.datetime.now() - datetime.timedelta(days=timedelta)).strftime(form)
    return (datetime.datetime.now() + datetime.timedelta(days=timedelta)).strftime(form)


def generate_date_minus_year_with_form(form: str):
    """
    Получить текущую дату минус год
    """
    return (datetime.datetime.now() - datetime.timedelta(days=365)).strftime(form)


def generate_date_plus_year_with_form(form: str):
    """
    Получить текущую дату плюс год
    """
    return (datetime.datetime.now() + datetime.timedelta(days=365)).strftime(form)


def generate_word() -> str:
    return Faker('ru_RU').word()

