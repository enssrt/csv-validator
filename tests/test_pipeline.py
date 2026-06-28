# tests/test_pipeline.py
import unittest
from pathlib import Path

# Импортируем наши функции для проверки
from source.csv_utils import normalize_cli_columns, check_required_columns
from source.validators import validate_price, validate_date
from main import run_pipeline

class TestCSVValidationPipeline(unittest.TestCase):

    def test_normalize_cli_columns(self):
        # Проверяем, что утилита правильно чистит и делит строку из терминала
        raw_input = "  NAME , PRICE , data_registered "
        expected = ["name", "price", "data_registered"]
        self.assertEqual(normalize_cli_columns(raw_input), expected)

    def test_validate_price_correct(self):
        # Проверяем валидатор цены на корректных данных
        is_ok, err = validate_price("100.50")
        self.assertTrue(is_ok)
        self.assertIsNone(err)

    def test_validate_price_incorrect(self):
        # Проверяем, что валидатор цены ловит ошибки
        is_ok, err = validate_price("-50")
        self.assertFalse(is_ok)
        self.assertIn("строго", err)

        is_ok_text, err_text = validate_price("not_a_number")
        self.assertFalse(is_ok_text)

    def test_validate_date_correct(self):
        # Проверяем валидатор даты на корректном формате
        is_ok, err = validate_date("2026-06-28")
        self.assertTrue(is_ok)
        self.assertIsNone(err)

    def test_validate_date_incorrect(self):
        # Проверяем валидатор даты на сломанном формате
        is_ok, err = validate_date("28/06/2026")
        self.assertFalse(is_ok)

    def test_check_required_columns_success(self):
        # Проверяем логику сравнения заголовков, если всё на месте
        file_header = ["name", "price", "date"]
        required = ["name", "price"]
        missing, status = check_required_columns(file_header, required)
        self.assertEqual(missing, [])
        self.assertEqual(status, "OK")

    def test_check_required_columns_missing(self):
        # Проверяем логику сравнения заголовков, если чего-то не хватает
        file_header = ["name", "date"]
        required = ["name", "price"]
        missing, status = check_required_columns(file_header, required)
        self.assertEqual(missing, ["price"])
        self.assertEqual(status, "ERROR")

if __name__ == "__main__":
    unittest.main()