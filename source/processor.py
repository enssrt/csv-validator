# source/processor.py

import csv
from source.csv_utils import read_csv_file, check_required_columns, normalize_header
from source.report_utils import generate_report
from source.validators import validate_price, validate_date
from pathlib import Path

def process_single_file(file_path, output_folder, current_columns):
    output_folder = Path(output_folder)
    file_path = Path(file_path)
    file_name = file_path.name

    result = {
        "file_name": file_name,
        "status": "UNKNOWN",
        "report_saved": False,
        "error_reason": None,
        "data_errors": []
    }

    header, data_row_count = read_csv_file(file_path)

    if header is None:
        result["status"] = "NOT_READ"
        result["error_reason"] = "файл не найден по указанному пути" if not file_path.exists() else "файл существует, но он абсолютно пустой"
        return result

    normalized_header = normalize_header(header)
    missing_columns, status = check_required_columns(normalized_header, current_columns)

    if status == "ERROR":
        result["status"] = "ERROR"
        result["error_reason"] = f"Отсутствуют обязательные колонки: {missing_columns}"
    else:
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row_idx, row in enumerate(reader, start=2):
                    norm_row = {normalize_header([k])[0]: v for k, v in row.items()}

                    if "price" in current_columns:
                        is_price_correct, price_err = validate_price(norm_row.get("price"))
                        if not is_price_correct:
                            result["data_errors"].append({"row": row_idx, "column": "price", "message": price_err})

                    if "date" in current_columns:
                        is_date_correct, date_err = validate_date(norm_row.get("date"))
                        if not is_date_correct:
                            result["data_errors"].append({"row": row_idx, "column": "date", "message": date_err})

        except Exception as e:
            result["status"] = "NOT_READ"
            result["error_reason"] = f"Ошибка при чтении строк файла: {str(e)}"
            return result

        if result["data_errors"]:
            result["status"] = "ERROR"
            result["error_reason"] = "Обнаружены ошибки значений в строках"
        else:
            result["status"] = "OK"
            result["error_reason"] = None
    # генерация отчета
    report_path = output_folder / f"report_{file_name}.txt"
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

    if result["data_errors"]:
        result["data_errors"] = [f"В строке {err['row']} ошибка {'цены' if err['column'] == 'price' else 'даты'}: {err['message']}" for err in result["data_errors"]]
    return result
 # Folder
def process_folder(input_folder, output_folder, current_columns):
    input_folder = Path(input_folder)
    results = []

    if not input_folder.is_dir():
        return results 
    # .iterdir вытаскивает полный путь для каждого файла
    for file_path in input_folder.iterdir():
        if file_path.suffix == ".csv":
            file_result = process_single_file(file_path, output_folder, current_columns)
            results.append(file_result)

    return results