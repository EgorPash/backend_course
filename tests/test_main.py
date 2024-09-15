import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch
from src.main import format_card, format_account, get_last_five_executed_operations, print_operations

class TestMain(unittest.TestCase):
    def test_format_card(self):
        self.assertEqual(format_card('Visa Classic 1234 56** **** 7890'), 'Visa ** **** 7890')
        self.assertEqual(format_card('MasterCard 1234 56** **** 7890'), 'MasterCard ** **** 7890')

    def test_format_card_with_missing_fields(self):
        self.assertEqual(format_card(''), '** **** ')
        self.assertEqual(format_card(None), '** **** ')

    def test_format_account_with_missing_fields(self):
        self.assertEqual(format_account(None), '** ****')
        self.assertEqual(format_account('abc'), '** ****')

    def test_get_last_five_executed_operations_with_empty_list(self):
        self.assertEqual(get_last_five_executed_operations([]), [])

    def test_format_account(self):
        self.assertEqual(format_account('12345678901234'), '** 1234')
        self.assertEqual(format_account(''), '** ****')
        self.assertEqual(format_account('abc'), '** ****')

    @patch('src.main.json.load')
    def test_get_last_five_executed_operations(self, mock_load):
        mock_load.return_value = [
            {'id': 1, 'state': 'EXECUTED', 'date': '2022-01-01T00:00:00.000000'},
            {'id': 2, 'state': 'EXECUTED', 'date': '2022-01-02T00:00:00.000000'},
            {'id': 3, 'state': 'EXECUTED', 'date': '2022-01-03T00:00:00.000000'},
            {'id': 4, 'state': 'EXECUTED', 'date': '2022-01-04T00:00:00.000000'},
            {'id': 5, 'state': 'EXECUTED', 'date': '2022-01-05T00:00:00.000000'},
            {'id': 6, 'state': 'CANCELED', 'date': '2022-01-06T00:00:00.000000'}
        ]
        self.assertEqual(len(get_last_five_executed_operations(mock_load.return_value)), 5)

        mock_load.return_value = []
        self.assertEqual(len(get_last_five_executed_operations(mock_load.return_value)), 0)

        mock_load.return_value = [
            {'id': 1, 'state': 'CANCELED', 'date': '2022-01-01T00:00:00.000000'},
            {'id': 2, 'state': 'CANCELED', 'date': '2022-01-02T00:00:00.000000'}
        ]
        self.assertEqual(len(get_last_five_executed_operations(mock_load.return_value)), 0)

    @patch('builtins.print')
    def test_print_operations(self, mock_print):
        operations = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589"
            }
        ]
        print_operations(operations)
        mock_print.assert_any_call("26.08.2019 Перевод организации")
        mock_print.assert_any_call("Maestro ** **** 5199 -> ** 9589")
        mock_print.assert_any_call("31957.58 руб.")


if __name__ == '__main__':
    unittest.main()