import os

from source.csv_utils import read_csv_file, check_required_columns, normalize_header
from source.report_utils import generate_report
from source.config import required_columns # ["name", "date", "price"]
from pathlib import Path

def process_single_file(file_path, output_folder): 
    
    # переменная из полного адресса пути файла, но мы его отрезали оставив только имя
    file_name = file_path.name
    # Создаем словарь для хранения результатов обработки файла
    result = {
        "file_name": file_name,
        "status": "UNKNOWN",
        "report_saved": False,
        "error_reason": None
    }

    header, data_row_count = read_csv_file(file_path)

    # Если файл не прочитался, определяем точную причину для отчета
    if header is None:
        result["status"] = "NOT_READ"
        
        if not file_path.exists():
            result["error_reason"] = "файл не найден по указанному пути"
        else:
            result["error_reason"] = "файл существует, но он абсолютно пустой"
        return result

    # Нормализуем заголовок и проверяем колонки
    normalized_header = normalize_header(header)        
    missing_columns, status = check_required_columns(normalized_header, required_columns)
    
    # Сохраняем статус проверки в словарь результатов
    result["status"] = status
    
    # Если колонки пропущены — сохраняем конкретику в словарь
    if status == "ERROR":
        result["error_reason"] = f"Отсутствуют обязательные колонки: {missing_columns}"

    report_path = output_folder / f"report_{file_name}.txt"

    # Пробуем сохранить отчет и записываем результат в словарь
    is_report_saved = generate_report(normalized_header, data_row_count, status, missing_columns, required_columns, report_path)

    result["report_saved"] = is_report_saved

    if not is_report_saved:
        result["status"] = "REPORT_ERROR"
        result["error_reason"] = "Не удалось записать файл отчета на диск"   
        return result
    
    return result

def process_folder(input_folder, output_folder):
    # превращаем папку в обьект адресса с помощью path
    input_folder = Path(input_folder)
    results = []
    # проверка существовании входной папки
    if not input_folder.is_dir():
        return results # если нет, возвращаем пустой список и заканчиваем
    
    # .iterdir вытаскивает полный путь для каждого файла
    for file_path in input_folder.iterdir():
        # проверка типа файла .csv
        if file_path.suffix == ".csv":

            # получаем итог файла через функцию
            file_result = process_single_file(file_path, output_folder)

            # кидаем в словарь список результатов файла
            results.append(file_result)

    return results