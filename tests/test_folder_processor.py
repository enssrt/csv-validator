
from source.processor import process_folder
    
def test_folder_combinated_type_of_files(tmp_path):
    current_columns = ["name", "price", "date"]
    # создаем исходную папку
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path_csv = input_folder / "test_01_correct.csv"
    file_path_png = input_folder / "test_01_correct.png"
    # по адрессу файла пишем в нем наши значниея
    file_path_csv.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    file_path_png.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    # выводим результаты каждого файла
    results = process_folder(input_folder, output_folder, current_columns)
    # утверждение, сравниваем с ожидаемыми результатами
    assert len(results) == 1
    assert results[0]["file_name"] == "test_01_correct.csv"
    assert results[0]["status"] == "OK"

def test_folder_not_exist(tmp_path):
    current_columns = ["name", "price", "date"]
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    expected_result = []
    actual_result = process_folder(input_folder, output_folder, current_columns)
    assert actual_result == expected_result

def test_folder_no_csv_exist(tmp_path):
    current_columns = ["name", "price", "date"]
    # создаем исходную папку
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    
    file_path_png = input_folder / "test_01_correct.png"
    file_path_png.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    
    expected_result = []
    actual_result = process_folder(input_folder, output_folder, current_columns)
    assert actual_result == expected_result
