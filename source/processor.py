# source/processor.py
import csv

from source.csv_utils import read_csv_file, check_required_columns, normalize_header
from source.report_utils import generate_report
from source.validators import validate_price, validate_date
from pathlib import Path

# Single file
def process_single_file(file_path, output_folder, current_columns): 
    
    # переменная из полного адресса пути файла, но мы его отрезали оставив только имя
    file_name = file_path.name
    # Создаем словарь для хранения результатов обработки файла
    result = {
        "file_name": file_name,
        "status": "UNKNOWN",
        "report_saved": False,
        "error_reason": None,
        "data_errors": None
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
    missing_columns, status = check_required_columns(normalized_header, current_columns)
    
    # Сохраняем статус проверки в словарь результатов
    result["status"] = status
    
    # Если колонки пропущены — сохраняем конкретику в словарь
    if status == "ERROR":
        result["error_reason"] = f"Отсутствуют обязательные колонки: {missing_columns}"
    else:
        with open(file_path, mode="r", encoding="utf-8") as file:
                # инструмент который читает и создает словари по ключам
                reader = csv.DictReader(file)
                # enumerate - это счетчик который считает каждую строку 
                # она с помощью reader читает, разделяет и ставит словарь 
                # и начинает со второй строки 
                # row_idx - это индекс каждой строки 
                # row это просто строка
                for row_idx, row in enumerate(reader, start=2):
                    # нормализируем ключи, оставляя значения неизменными 
                    # [k] делает из ключа список, а [0] достает из результата строку
                    norm_row = {normalize_header([k])[0]: v for k, v in row.items()}

                    # ПРОВЕРКА PRICE
                    if "price" in current_columns:
                        # достаем из строки нужный элемент по ее ключу
                        raw_price = norm_row.get("price")
                        # достаем итоговые значения с помощью функций
                        is_price_correct, price_err = validate_price(raw_price)
                        if not is_price_correct:
                            if result["data_errors"] is None:
                                result["data_errors"] = []
                            result["data_errors"].append(f"В строке {row_idx} ошибка цены: {price_err}")

                    # ПРОВЕРКА DATE
                    if "date" in current_columns:
                        raw_date = norm_row.get("date")
                        is_date_correct, date_err = validate_date(raw_date)
                        if not is_date_correct:
                            if result["data_errors"] is None:
                                result["data_errors"] = []
                            result["data_errors"].append(f"В строке {row_idx} ошибка даты: {date_err}")
                    
        if result["data_errors"] and len(result["data_errors"]) > 0:
            result["status"] = "ERROR"
            result["error_reason"] = "Обнаружены ошибки значений в строках"
        else:
            result["status"] = "OK"

    report_path = output_folder / f"report_{file_name}.txt"

    # Пробуем сохранить отчет и записываем результат в словарь
    is_report_saved = generate_report(
        normalized_header, 
        data_row_count, 
        result["status"],
        missing_columns, 
        current_columns, 
        report_path,
        result["data_errors"]
        )

    result["report_saved"] = is_report_saved

    if not is_report_saved:
        result["status"] = "REPORT_ERROR"
        result["error_reason"] = "Не удалось записать файл отчета на диск"   
        return result
    
    return result


 # Folder
def process_folder(input_folder, output_folder, current_columns):
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
            file_result = process_single_file(file_path, output_folder, current_columns)

            # кидаем в словарь список результатов файла
            results.append(file_result)

    return results