
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
        "error_reason": None
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
        "error_reason": "файл не найден по указанному пути"
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
        "error_reason": None
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
        "error_reason": "Не удалось записать файл отчета на диск"
    }
    # настоящий результат
    actual_file_result = process_single_file(file_path, output_folder)
    # сравнение результатов
    assert actual_file_result == expected_file_result