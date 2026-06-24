
from source.config import folder_path, reports_dir, required_columns
from source.processor import process_single_file, process_folder
from pathlib import Path
import argparse


def main():
    # создаем инструмент для разбора терминала
    parser = argparse.ArgumentParser(description="Программа для автоматической валидации CSV таблиц")
    # создаем аргумент --input чтобы код воспринимал его
    parser.add_argument('--input',type=str, required=True, help="Путь к исходной папки с CSV")
    # создаем аргумент --output чтобы код воспринимал его
    parser.add_argument('--output',type=str, required=True, help="Путь папки для отчетов с CSV")
    # читаем аргуементы из консоли и раскладываем по переменным
    args = parser.parse_args()
    # делаем умные обьекты путей 
    input_folder = Path(args.input)
    output_folder = Path(args.output)

    # Проверяем, существует ли папка с исходными файлами
    if not input_folder.is_dir():
        print(f"Ошибка: Папки {folder_path} не существует")
        return
    
    # Создаем папку для отчетов, если её еще нет
    print(f"Подготовка папки для отчетов: {reports_dir}")
    output_folder.mkdir(parents=True, exist_ok=True)

    print(f"происходит обработка папки: {folder_path}")

    stats = run_pipeline(input_folder, output_folder)

    # финальный отчет
    print("\n" + "="*40)
    print("         ФИНАЛЬНАЯ СТАТИСТИКА")
    print("="*40)
    
    if stats["total_files"] == 0:
        print("Внимание: в указанной папке не найдено ни одного CSV-файла!")
    else:
        print(f"Всего найдено и проверено файлов:    {stats['total_files']}")
        print(f"Успешно валидировано (OK):           {stats['OK']}")
        print(f"Файлов с ошибками (ERROR):           {stats['ERROR']}")
        print(f"Не удалось прочитать (NOT_READ):     {stats['NOT_READ']}")
        print(f"Ошибка записи отчета (REPORT_ERROR): {stats['REPORT_ERROR']}")
        
    print("="*40)
    print("Выполнение программы закончено.")


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

if __name__ == "__main__":
    main()