# tests/test_validators.py

from source.validators import validate_date, validate_price
from source.processor import process_single_file
# price
def test_validate_price_ok():
    price = "123"
    expected_result = True, None
    actual_result = validate_price(price)
    assert expected_result == actual_result

def test_validate_price_err():
    price = "-123"
    expected_result = False, "Цена должна быть строго больше нуля"
    actual_result = validate_price(price)
    assert expected_result == actual_result

def test_validate_price_err_empty():
    price = " "
    expected_result = False, "Значение не является числом"
    actual_result = validate_price(price)
    assert expected_result == actual_result

def test_validate_price_zero():
    price = "0"
    expected_result = False, "Цена должна быть строго больше нуля"
    actual_result = validate_price(price)
    assert expected_result == actual_result

def test_validate_price_word():
    price = "word"
    expected_result = False, "Значение не является числом"
    actual_result = validate_price(price)
    assert expected_result == actual_result


# date
def test_validate_date_ok():
    date = "2000-10-30"
    expected_result = True, None
    actual_result = validate_date(date)
    assert expected_result == actual_result

def test_validate_date_err():
    date = "20200-10-30"
    expected_result = False, "Некорректный формат даты или несуществующая дата"
    actual_result = validate_date(date)
    assert expected_result == actual_result

def test_validate_date_err_2():
    date = "2020-13-30"
    expected_result = False, "Некорректный формат даты или несуществующая дата"
    actual_result = validate_date(date)
    assert expected_result == actual_result

def test_validate_date_err_3():
    date = "2020/10/30"
    expected_result = False, "Некорректный формат даты или несуществующая дата"
    actual_result = validate_date(date)
    assert expected_result == actual_result

