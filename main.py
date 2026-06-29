# main.py


from source.csv_utils import normalize_cli_columns
from source.config import REQUIRED_COLUMNS
from source.processor import process_folder
from pathlib import Path
import argparse
import sys

# проверка и сборка входных данных
def parse_args(args_list=None):
    # создаем инструмент для чтения терминала
        parser = argparse.ArgumentParser(description="Программа для автоматической валидации CSV таблиц")
        # создаем аргументы чтобы код мог их воспринимать
        parser.add_argument('--input',type=str, required=True, help="Путь к исходной папки с CSV")
        parser.add_argument('--output',type=str, required=True, help="Путь папки для отчетов с CSV")
        parser.add_argument('--columns',type=str, required=False, help="Список обязательных колонок через запятую")
        # читаем аргуементы из консоли и раскладываем по переменным
        args = parser.parse_args(args_list)
        return args

# главный движок
def execute_pipeline(args):
        # делаем умные обьекты путей 
        input_folder = Path(args.input)
        output_folder = Path(args.output)

        if args.columns:
            norm_cli_columns = normalize_cli_columns(args.columns)
        else:
            print("Вы не указали обязательные колонки, обязательные колонки будут выбраны по умолчанию (name,date,price)")
            norm_cli_columns = REQUIRED_COLUMNS


        # Проверяем, существует ли папка с исходными файлами
        if not input_folder.is_dir():
            print(f"Ошибка: Папки {input_folder} не существует")
            return 1
        
        # Создаем папку для отчетов, если её еще нет
        print(f"Подготовка папки для отчетов: {output_folder}")
        output_folder.mkdir(parents=True, exist_ok=True)

        print(f"происходит обработка папки: {input_folder}")

        stats = run_pipeline(input_folder, output_folder, norm_cli_columns)

        # финальный отчет
        print("\n" + "="*40)
        print("         ФИНАЛЬНАЯ СТАТИСТИКА")
        print("="*40)
        
        if stats["total_files"] == 0:
            print("Внимание: в указанной папке не найдено ни одного CSV-файла!")
        else:
            print(f" Всего найдено и проверено файлов:    {stats['total_files']}")
            print(f" Успешно валидировано (OK):           {stats['OK']}")
            print(f" Файлов с ошибками (ERROR):           {stats['ERROR']}")
            print(f" Не удалось прочитать (NOT_READ):     {stats['NOT_READ']}")
            print(f" Ошибка записи отчета (REPORT_ERROR): {stats['REPORT_ERROR']}")
            
        print("="*40)
        print("Выполнение программы закончено.")
        return 0

# связка в конвейер
def run_pipeline(input_folder, output_folder, current_columns):
    if current_columns is None:
        current_columns = REQUIRED_COLUMNS
    results = process_folder(input_folder, output_folder, current_columns)
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


def main(args_list=None):
    args = parse_args(args_list)    
    return execute_pipeline(args)


if __name__ == "__main__":
    sys.exit(main())

