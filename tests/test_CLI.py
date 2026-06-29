# tests/test_CLI.py

from main import main
import pytest

def test_exit_0(tmp_path):

    input_folder = tmp_path / "input"
    input_folder.mkdir()

    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    # проверяем возвращаемый код
    exit_code = main(["--input", str(input_folder), "--output", str(output_folder)])
    assert exit_code == 0


def test_exit_1(tmp_path):
    # даем путь папки но не создаем ее. не существует
    input_folder = tmp_path / "input"

    # создаем папку для отчетов
    output_folder = tmp_path / "output"
    output_folder.mkdir()
    
    exit_code = main(["--input", str(input_folder), "--output", str(output_folder)])
    assert exit_code == 1