import csv

def read_csv_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Чтение CSV файла через встроенный модуль
            reader = csv.reader(file)
            # Читаем первую строку (заголовок)
            header = next(reader)
            # Считаем количество строк с данными
            data_row_count = 0
            for row in reader:
                data_row_count += 1
        return header, data_row_count
    except (FileNotFoundError, StopIteration):
        # Если файл пустой или не найден, возвращаем None (вывод ошибки будет в main)
        return None, 0
    
def normalize_header(header):
    # Приводим названия колонок к нижнему регистру и убираем пробелы по краям
    normalized_header = []
    for column in header:
        normalized_column = column.strip().lower()
        normalized_header.append(normalized_column)   
    return normalized_header


def check_required_columns(normalized_header, required_columns):
    # Ищем, каких обязательных колонок не хватает в файле
    missing_columns = []
    for required_column in required_columns:
        if required_column not in normalized_header:
            missing_columns.append(required_column)
    # Меняем статус в зависимости от наличия ошибок
    if len(missing_columns) > 0:
        status = "ERROR"
    else:
        status = "OK" 
    return missing_columns, status