import functools
import sys
from allure import testcase, story, severity, description, title as allure_title


def get_params_from_cmd() -> dict:
    """
    Функция позволяет получить список параметров словарём.
    """
    params = {}
    if len(sys.argv) > 1:
        for param in sys.argv:
            if '--' and '=' in param:
                w1, w2 = param.split('=')
                params[w1] = w2
    return params


def allure_collect_decorator(
                                title,
                                description_case,
                                severity_allure,
                                url_case="Ссылки_нет",
                                name_url_case="Ссылка на тест-кейс",
                                allure_story="Общий функционал",
                                ):
    """
    Функция предназначена для объединения декораторов библиотек
    allure и testit.
    """
    def inner(func):
        @testcase(url=url_case,
                  name=name_url_case)
        @description(description_case)
        @story(allure_story)
        @allure_title(title)
        @severity(severity_allure)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return inner

