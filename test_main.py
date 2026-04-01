import unittest
import runpy
from unittest.mock import patch
from main import calculate_sum_and_average, get_numbers_from_user

class TestCalculateFunctions(unittest.TestCase):

    def test_valid_numbers(self):
        self.assertEqual(calculate_sum_and_average([1, 2, 3]), (6, 2.0))

    def test_empty_list(self):
        with self.assertRaises(ValueError) as context:
            calculate_sum_and_average([])
        self.assertEqual(str(context.exception), "Dãy số không được rỗng nha.")

    def test_negative_numbers(self):
        with self.assertRaises(ValueError):
            calculate_sum_and_average([1, -2, 3])

    def test_non_numeric_input(self):
        with self.assertRaises(ValueError):
            calculate_sum_and_average(["a", "b", "c"])

    def test_get_numbers_from_user_valid_input(self):
        with patch("builtins.input", return_value="1 2 3"):
            self.assertEqual(get_numbers_from_user(), [1, 2, 3])

    def test_get_numbers_from_user_retry_after_invalid(self):
        with patch("builtins.input", side_effect=["a b", "4 5"]):
            with patch("builtins.print") as mock_print:
                self.assertEqual(get_numbers_from_user(), [4, 5])
                self.assertTrue(mock_print.called)

    def test_get_numbers_from_user_retry_after_non_positive(self):
        with patch("builtins.input", side_effect=["0 2", "3 4"]):
            with patch("builtins.print") as mock_print:
                self.assertEqual(get_numbers_from_user(), [3, 4])
                self.assertTrue(mock_print.called)

    def test_main_success_path(self):
        with patch("builtins.input", return_value="2 4"):
            with patch("builtins.print") as mock_print:
                runpy.run_module("main", run_name="__main__")
                mock_print.assert_any_call("Tổng: 6, Trung bình: 3.0")

    def test_main_error_path(self):
        with patch("builtins.input", return_value=""):
            with patch("builtins.print") as mock_print:
                runpy.run_module("main", run_name="__main__")
                mock_print.assert_any_call("Lỗi: Dãy số không được rỗng nha.")
