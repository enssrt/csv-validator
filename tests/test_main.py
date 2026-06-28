# tests/test_main.py


from main import run_pipeline
from pathlib import Path
# python -m pytest tests/test_main.py

def test_run_OK(tmp_path):
    # создаем исходную папку
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path_csv = input_folder / "test_01_correct.csv"
    file_path_png = input_folder / "test_02_ignored_type.png"
    # по адрессу файла пишем в нем наши значниея
    file_path_csv.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    file_path_png.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    
    expected_stats = {
    "total_files": 1,
    "OK": 1,
    "ERROR": 0,
    "NOT_READ": 0,
    "REPORT_ERROR": 0
    }
    # выводим результаты 
    actual_stats =  run_pipeline(input_folder, output_folder)
    assert expected_stats == actual_stats

def test_run_ERROR(tmp_path):
    # создаем исходную папку
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path_csv = input_folder / "test_01_error.csv"
    # по адрессу файла пишем в нем наши значниея
    file_path_csv.write_text("name,date\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    
    expected_stats = {
    "total_files": 1,
    "OK": 0,
    "ERROR": 1,
    "NOT_READ": 0,
    "REPORT_ERROR": 0
    }
    # выводим результаты 
    actual_stats =  run_pipeline(input_folder, output_folder)
    assert expected_stats == actual_stats

def test_run_REPORT_ERROR(tmp_path):
    # создаем исходную папку
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    # создаем папку для отчетов
    output_folder = tmp_path / "output_error"
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path_csv = input_folder / "test_01_correct.csv"
    # по адрессу файла пишем в нем наши значниея
    file_path_csv.write_text("name,date,price\nApple,2026-06-17,150\nBanana,2026-06-17,90")
    
    expected_stats = {
    "total_files": 1,
    "OK": 0,
    "ERROR": 0,
    "NOT_READ": 0,
    "REPORT_ERROR": 1
    }
    output_folder.chmod(0o444)
    # выводим результаты 
    actual_stats =  run_pipeline(input_folder, output_folder)
    output_folder.chmod(0o755)
    assert expected_stats == actual_stats

def test_run_NOT_READ(tmp_path):
    # создаем исходную папку
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    # даем путь к файлу при этом записывая называние самого файла
    file_path_csv = input_folder / "test_empty.csv"
    # по адрессу файла пишем в нем наши значниея
    file_path_csv.write_text("")
    expected_stats = {
    "total_files": 1,
    "OK": 0,
    "ERROR": 0,
    "NOT_READ": 1,
    "REPORT_ERROR": 0
    }
    # выводим результаты 
    actual_stats =  run_pipeline(input_folder, output_folder)
    assert expected_stats == actual_stats