# soure/report_utils.py

def generate_report(normalized_header, data_row_count, status, missing_columns, required_columns, report_path, data_errors):
    try:
        # Защита от None: если валидация строк не проводилась, подменяем None на пустой список,
        # чтобы функция len(data_errors) ниже не выдала ошибку.
        data_errors = data_errors or []
        # Записываем результаты проверки в текстовый файл отчета
        with open(report_path, "w", encoding="utf-8") as report_file:
            # шапка отчета
            report_file.write("=" * 50 + "\n")
            report_file.write("              ОТЧЕТ ОБ ОБРАБОТКЕ ФАЙЛА            \n")
            report_file.write("=" * 50 + "\n")
            report_file.write(f"СТАТУС: {status} \n")
            # СЦЕНАРИЙ 1 (ФАЙЛ ПУСТОЙ ИЛИ ПОВРЕЖДЕН) - "NOT_READ"
            if status == "NOT_READ":
                report_file.write(f"КОЛИЧЕСТВО СТРОК С ДАННЫМИ: Неизвестно (ошибка чтения)\n")
                report_file.write("-" * 50 + "\n")
                report_file.write("Ошибка: Не удалось прочитать структуру CSV-файла \n")
                report_file.write("Файл пуст, поврежден или заблокирован другим процессом. \n")
                report_file.write("=" * 50 + "\n")
                return True
            # Если файл прочитался то пишем кол-во строк данных
            report_file.write(f"КОЛИЧЕСТВО СТРОК С ДАННЫМИ: {data_row_count} \n")
            # ПРОВЕРКА СТРУКТУРЫ КОЛОНОК
            report_file.write("-" * 50 + "\n")
            report_file.write("1. ПРОВЕРКА СТРУКТУРЫ КОЛОНОК \n")
            report_file.write("-" * 50 + "\n")
            report_file.write(f"Колонки в файле: {normalized_header}\n")
            report_file.write(f"Количество колонок в файле {len(normalized_header)}\n")
            # СЦЕНАРИЙ 2 (ПРОПУЩЕННЫ ОБЯЗ КОЛОНКИ) - "ERROR"
            if len(missing_columns) > 0:
                report_file.write("Статус колонок: ОШИБКА (отсутствуют требуемые колонки) \n")
                report_file.write(f"Отсутствующие колонки: {missing_columns}\n")
                report_file.write(f"Ожидаемый список колонок для проверки: {required_columns}\n")
                report_file.write("=" * 50 + "\n")
                report_file.write("2. ПРОВЕРКА ДАННЫХ (построчно)\n")
                report_file.write("=" * 50 + "\n")
                report_file.write("Валидация строк не производилась из-за ошибки структуры колонок. \n")
                report_file.write("=" * 50 + "\n")
                return True 
            # СЦЕНАРИЙ 3 ОШИБОК НЕТ - "OK"
            report_file.write("Статус колонок: ОК (все обязательные колонки присутствуют)\n")
            report_file.write(f"Проверяемые колонки: {required_columns}\n")
            report_file.write("=" * 50 + "\n")
            report_file.write("2. ПРОВЕРКА ДАННЫХ (построчно)\n")
            report_file.write("=" * 50 + "\n")
            if len(data_errors) > 0:
                report_file.write(f"ОБНАРУЖЕНО ОШИБОК В СТРОКАХ: {len(data_errors)} \n")
                report_file.write("ИНФОРМАЦИЯ ОБ ОШИБКАХ: \n")
                for err in data_errors:
                    if err["column"] == "price":
                        report_file.write(f"В строке {err['row']} ошибка цены: {err['message']}\n")
                    elif err["column"] == "date":
                        report_file.write(f"В строке {err['row']} ошибка даты: {err['message']}\n")
            else:
                report_file.write("ОБНАРУЖЕНО ОШИБОК В СТРОКАХ: 0\n")
                report_file.write("Ошибок в данных строк не обнаружено.\n")
            report_file.write("=" * 50 + "\n")

        return True
    except Exception as e:
        print(f"He удалось сохранить отчет на диск: {e}")
        return False
