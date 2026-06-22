

# ипортируем настройки из конфигурационного модуля
from source.config import folder_path, reports_dir
# Импортируем функцию-обработчик сценария
from source.processor import process_single_file, process_folder
from source.csv_utils import check_required_columns, normalize_header, read_csv_file
from pathlib import Path

def main():
    input_folder = Path(folder_path)
    output_folder = Path(reports_dir)

    # Проверяем, существует ли папка с исходными файлами
    if not input_folder.is_dir():
        print(f"Ошибка: Папки {folder_path} не существует")
        return
    
    # Создаем папку для отчетов, если её еще нет
    print(f"Подготовка папки для отчетов: {reports_dir}")
    output_folder.mkdir(parents=True, exist_ok=True)

    # Получаем список всех файлов в папке
    all_files = list(input_folder.iterdir())
    print(f"происходит обработка папки: {folder_path}")

    # Счетчики для общей статистики
    csv_count = 0
    csv_success = 0
    csv_failed = 0

    for file_path in all_files: 

        # Обрабатываем только файлы с расширением .csv
        if file_path.suffix != ".csv":
            continue

        csv_count += 1

        # Запускаем обработку одного файла и получаем словарь с результатами
        file_result = process_single_file(file_path, output_folder)

        print(f"статус проверки: ", {file_result["status"]})

        # Проверяем по словарю, сохранился ли отчет, и обновляем счетчики
        if file_result["report_saved"]:
            print(f"отчет для {file_path.name} успешно сохранен")
            csv_success += 1
        else:
            print(f"не удалось сохранить отчет для файла {file_path.name}, причина ошибки: {file_result['error_reason']} ")
            csv_failed += 1
    print("\n")
    
    # Выводим финальную общую статистику в консоль
    if csv_count == 0:
        print("Внимание: в указанной папке не найдено ни одного CSV-файла для обработки!")
    else:
        print("Обработка завершена. \n")
        print(f"всего найдено CSV файлов: {csv_count}")
        print(f"количество обработанных CSV файлов: {csv_success}")
        print(f"количество необработанных CSV файлов: {csv_failed}")   
    print("выполнение программы закончено")

if __name__ == "__main__":
    main()

def run_pipeline(input_folder, output_folder):

    results = process_folder(input_folder, output_folder)
    # словарь статистики по всем файлам 
    stats = {
        "total_files": 0,
        "OK": 0,
        "ERROR": 0,
        "NOT_READ": 0,
        "REPORT_ERROR": 0        
    }

    for result in results:
        # достаем значение статуса из словаря результатов одного файла
        status = result.get("status")

        if status in stats:
            # если есть статус то увеличиваем его счетчик на единицу
            stats[status] += 1

            stats["total_files"] += 1
    return stats