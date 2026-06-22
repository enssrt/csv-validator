
def generate_report(normalized_header, data_row_count, status, missing_columns, required_columns, report_path):
    try:
        # Записываем результаты проверки в текстовый файл отчета
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write("колонки в файле: " + str(normalized_header) + "\n")
            report_file.write("количество колонок в файле: " + str(len(normalized_header)) + "\n")
            report_file.write("количество строк данных: " + str(data_row_count) + "\n")
            report_file.write("статус проверки: " + str(status) + "\n")    
            
            # Текст отчета меняется в зависимости от статуса проверки
            if status == "ERROR":
                report_file.write("отсутствующие колонки: " + str(missing_columns) + "\n")
                report_file.write("количество отсутствующих колонок: " + str(len(missing_columns)) + "\n")
            else:
                report_file.write("обязательные колонки найдены: " + str(required_columns) + "\n")
                report_file.write("количество обязательных найденных колонок: " + str(len(required_columns)) + "\n")
        return True
    except Exception as e:
        print(f"He удалось сохранить отчет на диск: {e}")
        return False
