import unittest
from unittest.mock import patch, Mock
import requests_mock
from joke_machine import main

from joke_machine import (get_joke_api,
                          get_joke_type,
                          get_joke,
                          BASE_URL,
                          )


class ComponentTests(unittest.TestCase):

    @requests_mock.mock()
    def test_end_to_end_single(self, m):
        m.get(BASE_URL, text='{"type": "single", "joke": "Just a test"}')
        joke_api = get_joke_api()
        joke_type = get_joke_type(joke_api)
        joke = get_joke(joke_api, joke_type)
        self.assertEqual(joke, "Just a test")

    @requests_mock.mock()
    def test_end_to_end_twopart(self, m):
        m.get(BASE_URL, text='{"type": "twopart", "setup": "Setup", "delivery": "Delivery"}')
        joke_api = get_joke_api()
        joke_type = get_joke_type(joke_api)
        joke = get_joke(joke_api, joke_type)
        self.assertEqual(joke, 'Setup\nDelivery')

    @patch('joke_machine.argument_parser')
    def test_main_with_zero_jokes(self, mock_argument_parser):
        with self.assertRaises(ValueError):
            mock_argument_parser.return_value = Mock(number_of_jokes=0)
            main()

    @patch('joke_machine.argument_parser')
    def test_main_with_one_joke(self, mock_argument_parser):
        mock_argument_parser.return_value = Mock(number_of_jokes=1)
        with self.assertLogs('joke_machine', level='INFO') as cm:  # assuming the print logs are captured at INFO level
            main()
        self.assertEqual(len(cm.output), 1)  # Expect one joke to be printed.

    @patch('joke_machine.argument_parser')
    def test_main_with_two_jokes(self, mock_argument_parser):
        mock_argument_parser.return_value = Mock(number_of_jokes=2)
        with self.assertLogs('joke_machine', level='INFO') as cm:  # assuming the print logs are captured at INFO level
            main()
        self.assertEqual(len(cm.output), 2)  # Expect two jokes to be printed.


if __name__ == '__main__':
    unittest.main()
