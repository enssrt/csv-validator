# tests/test_file_processor.py

from pathlib import Path
from source.processor import process_single_file

def test_file_full_correct(tmp_path):
    # даем переменную папке с названием + что она временная
    output_folder = tmp_path / "Folder"
    # создаем папку
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path = output_folder / "test_01_correct.csv"
    # по адрессу файда пишем в нем наши значниея
    file_path.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    # ожидаемый результат
    expected_file_result = {
        "file_name": "test_01_correct.csv",
        "status": "OK",
        "report_saved": True,
        "error_reason": None,
        "data_errors": None
    }
    # настоящий результат
    actual_file_result = process_single_file(file_path, output_folder)
    # сравнение результатов
    assert actual_file_result == expected_file_result

def test_file_no_files(tmp_path):
    # даем переменную папке с названием + что она временная
    output_folder = tmp_path / "Folder"
    # создаем папку
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path = output_folder / "not_exist.csv"
    # ожидаемый результат
    expected_file_result = {
        "file_name": "not_exist.csv",
        "status": "NOT_READ",
        "report_saved": False,
        "error_reason": "файл не найден по указанному пути",
        "data_errors": None
    }
    # настоящий результат
    actual_file_result = process_single_file(file_path, output_folder)
    # сравнение результатов
    assert actual_file_result == expected_file_result
        
def test_file_full_ignor_no_csv(tmp_path):
    # даем переменную папке с названием + что она временная
    output_folder = tmp_path / "Folder"
    # создаем папку
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path = output_folder / "test_01_correct.png"
    # создаем файл на диске чтобы он физически существовал
    file_path.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    # ожидаемый результат
    expected_file_result = {
        "file_name": "test_01_correct.png",
        "status": "OK",
        "report_saved": True,
        "error_reason": None,
        "data_errors": None
    }
    # настоящий результат
    actual_file_result = process_single_file(file_path, output_folder)
    # сравнение результатов
    assert actual_file_result == expected_file_result

def test_file_no_folder(tmp_path):
    # даем переменную папке с названием + что она временная
    output_folder = tmp_path / "Folder"

    # нет папки для теста

    # даем путь к файлу при этом записывая называние самого файла
    file_path = tmp_path / "test_01_correct.csv"
    # по адрессу файда пишем в нем наши значниея
    file_path.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    # ожидаемый результат
    expected_file_result = {
        "file_name": "test_01_correct.csv",
        "status": "REPORT_ERROR",
        "report_saved": False,
        "error_reason": "Не удалось записать файл отчета на диск",
        "data_errors": None
    }
    # настоящий результат
    actual_file_result = process_single_file(file_path, output_folder)
    # сравнение результатов
    assert actual_file_result == expected_file_result

def test_process_single_file_error_price_data(tmp_path):
    """Тест на интеграцию валидатора цены: колонки ОК, но цена битая + проверка отчета"""
    output_folder = tmp_path / "Folder"
    output_folder.mkdir()
    file_path = output_folder / "test_error_price.csv"
    file_path.write_text("name,date,price\nApple,2026-06-17,-150", encoding="utf-8")
    
    expected_result = {
        "file_name": "test_error_price.csv",
        "status": "ERROR",
        "report_saved": True,
        "error_reason": "Обнаружены ошибки значений в строках",
        "data_errors": ["В строке 2 ошибка цены: Цена должна быть строго больше нуля"]
    }
    
    actual_result = process_single_file(file_path, output_folder)
    assert actual_result == expected_result

    report_path = output_folder / f"report_{file_path.name}.txt" 
    assert report_path.exists(), "Файл отчета должен физически создаться!"
    
    report_content = report_path.read_text(encoding="utf-8")

    assert "ОБНАРУЖЕНО ОШИБОК В СТРОКАХ: 1" in report_content
    assert "В строке 2 ошибка цены:" in report_content
    
    assert "Валидация строк не производилась из-за критической ошибки структуры" not in report_content


def test_process_single_file_error_date_data(tmp_path):
    """Тест на интеграцию валидатора даты: колонки ОК, но дата битая + проверка отчета"""
    output_folder = tmp_path / "Folder"
    output_folder.mkdir()
    file_path = output_folder / "test_error_date.csv"
    file_path.write_text("name,date,price\nBanana,2026-99-17,90", encoding="utf-8")
    
    expected_result = {
        "file_name": "test_error_date.csv",
        "status": "ERROR",
        "report_saved": True,
        "error_reason": "Обнаружены ошибки значений в строках",
        "data_errors": ["В строке 2 ошибка даты: Некорректный формат даты или несуществующая дата"]
    }
    
    actual_result = process_single_file(file_path, output_folder)
    assert actual_result == expected_result

    report_path = output_folder / f"report_{file_path.name}.txt"
    assert report_path.exists()
    
    report_content = report_path.read_text(encoding="utf-8")
    
    assert "ОБНАРУЖЕНО ОШИБОК В СТРОКАХ: 1" in report_content
    assert "В строке 2 ошибка даты:" in report_content
    assert "Валидация строк не производилась из-за критической ошибки структуры" not in report_content