import allure


def check_that_data_is_not_equal(expected, received, description='Нету'):
    with allure.step(f'Ожидаемый {expected} != {received}'):
        assert expected != received, f'Ожидаемый результат "{expected}" != "{received}". Описание: {description}'


def check_that_data_is_equal(expected: any, received: any, description: str = "Нету"):
    with allure.step("Проверка, что ожидаемый результат равен полученному"):
        with allure.step(f"{expected} == {received}"):
            assert expected == received, f'Ожидаемый "{expected}" == "{received}" Описание: "{description}"'


def check_that_first_more_than_second(first, second, description: str = "Нету"):
    assert first > second, f'Первый элемент "{first}" не больше, чем второй элемент "{second}". Описание: "{description}"'


def check_that_data_present_in_received(expected, received, description: str = "Нету"):
    with allure.step(f"Проверяем, что {expected} есть в {received}"):
        assert expected in received, f'Ожидаемого "{expected}" нету в полученном "{received}". Описание: {description}'


def check_that_data_not_present_in_received(expected, received, description: str = "Нету"):
    with allure.step(f"Проверяем, что {expected} нет в {received}"):
        assert expected not in received, f'Ожидаемый "{expected}" есть в полученном "{received}". Описание: {description}'


def check_that_expected_equal_all_list(expected, received):
    assert all(expected == check for check in received)


def check_that_first_less_then_second(first, second, description: str = "Нету"):
    assert first < second, f"Первый элемент '{first}' не меньше и не равен второму элементу '{second}'.Описание: {description}"


def check_that_data_is_true(data: bool, description: str = "Нету"):
    with allure.step("Проверка, что ожидаемый результат: Истина"):
        assert data, f"Полученные данные: '{data}'. Описание: '{description}'"


def check_that_data_is_false(data: bool, description: str = "Нету"):
    with allure.step("Проверка, что ожидаемый результат: Ложь"):
        assert not data, f"Полученные данные: '{data}'. Описание: '{description}'"


def check_that_str_in_list_some(expected: str,
                                received: list,
                                description: str = "Нету"):
    """
    Функция проходит по элементам списка и проверяет, есть ли вхождение строки в элемент списка.
    Если нет, то вызывает assert False
    """

    with allure.step(f"Проверяем, что ожидаемый результат: '{expected}', есть в полученном списке: '{received}'"):
        result = False
        for word in received:
            if expected in word:
                result = True
        assert result, f' Ожидаемого результата: "{expected}", нет в :"{received}". Описание: "{description}"'
