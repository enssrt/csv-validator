from source.csv_utils import normalize_header, check_required_columns

# тестовая функция для проверки
def test_normalize_header_combined():
    # входные данные для теста
    dirty_input = [" Name", "DATE", "price"]
    # ожидаемый результат
    expected_output = ["name", "date", "price"]
    # результат входных данных
    actual_output = normalize_header(dirty_input)
    # проверяем с помощью утверждения assert
    assert actual_output == expected_output

def test_normalize_header_spaces():
    # входные данные для теста
    dirty_input = [" name ", "  date  ", "price  "]
    # ожидаемый результат
    expected_output = ["name", "date", "price"]
    # результат входных данных
    actual_output = normalize_header(dirty_input)
    # проверяем с помощью утверждения assert
    assert actual_output == expected_output

def test_normalize_header_case():
    # входные данные для теста
    dirty_input = ["NAME", "DAte", "price"]
    # ожидаемый результат
    expected_output = ["name", "date", "price"]
    # результат входных данных
    actual_output = normalize_header(dirty_input)
    # проверяем с помощью утверждения assert
    assert actual_output == expected_output


def test_check_required_columns_all_present():
    # входные данные для теста + условие
    normalized_header = ["name", "date","price"]
    required_columns = ["name", "date", "price"]
    # ожидаемый результат   
    expected_output = ([], "OK")
    # результат входных данных
    actual_output = check_required_columns(normalized_header, required_columns)
    # проверяем с помощью утверждения assert
    assert actual_output == expected_output

def test_check_required_columns_missing_one():
    # входные данные для теста + условие
    normalized_header = ["name", "price"]
    required_columns = ["name", "date", "price"]
    # ожидаемый результат
    expected_output = (["date"], "ERROR")
    # результат входных данных
    actual_output = check_required_columns(normalized_header, required_columns) 
    # проверяем с помощью утверждения assert
    assert actual_output == expected_output

def test_check_required_columns_missing_two():
    # входные данные для теста + условие
    normalized_header = ["name"]
    required_columns = ["name", "date", "price"]
    # ожидаемый результат
    expected_output = (["date","price"], "ERROR")
    # результат входных данных
    actual_output = check_required_columns(normalized_header, required_columns) 
    # проверяем с помощью утверждения assert
    assert actual_output == expected_output
