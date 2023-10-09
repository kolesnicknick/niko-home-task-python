import unittest
import requests_mock
from unittest import mock

from joke_machine import (ConnectionToJokeAPI,
                          argument_parser,
                          error_handler,
                          get_joke_api,
                          get_joke_type,
                          get_joke,
                          joke_machine_runner,
                          BASE_URL,
                          )


class TestConnectionToJokeAPI(unittest.TestCase):
    @requests_mock.mock()
    def test_init(self, m):
        m.get(BASE_URL, text='{"type": "single", "joke": "Just a test"}')
        conn = ConnectionToJokeAPI()
        self.assertIn('joke', conn.joke_api.json())


class TestFunctions(unittest.TestCase):
    # Argument parser
    def test_argument_parser_default(self):
        args = argument_parser()
        self.assertEqual(args.number_of_jokes, 1)

    def test_argument_parser_multiple_number(self):
        with mock.patch('sys.argv', ['prog_name', '-n', '3']):
            args = argument_parser()
            self.assertEqual(args.number_of_jokes, 3)

    def test_argument_parser_negative(self):
        with mock.patch('sys.argv', ['prog_name', '-n', '-1']):
            args = argument_parser()
            self.assertEqual(args.number_of_jokes, -1)

    def test_argument_parser_empty(self):  # Should fail - functionality not implemented yet
        with mock.patch('sys.argv', ['prog_name', '-n', '']):
            with self.assertRaises(ValueError):
                argument_parser()

    # Error handler
    def test_error_handler(self):
        with self.assertRaises(ValueError):
            error_handler("Test Error")

    # Get Joke api
    @requests_mock.mock()
    def test_get_joke_api(self, m):
        m.get(BASE_URL, text='{"type": "single", "joke": "Just a test"}')
        joke_api = get_joke_api()
        self.assertIn('joke', joke_api.json())

    # Get Joke type
    def test_get_joke_type_single(self):
        mock_response = type('', (), {})()
        mock_response.json = lambda: {'type': 'single'}
        self.assertEqual(get_joke_type(mock_response), "single")

    def test_get_joke_type_twopart(self):
        mock_response = type('', (), {})()
        mock_response.json = lambda: {'type': 'twopart'}
        self.assertEqual(get_joke_type(mock_response), "twopart")

    def test_get_joke_type_wrong_arg(self):  # Should fail - functionality not implemented yet
        with self.assertRaises(ValueError):
            mock_response = type('', (), {})()
            mock_response.json = lambda: {'type': 'threepart'}
            get_joke_type(mock_response)

    # Get Joke
    def test_get_joke_single(self):
        mock_response = type('', (), {})()
        mock_response.json = lambda: {'type': 'single', 'joke': 'This is a joke'}
        self.assertEqual(get_joke(mock_response, 'single'), 'This is a joke')

    def test_get_joke_twopart(self):
        mock_response = type('', (), {})()
        mock_response.json = lambda: {'type': 'twopart', 'setup': 'Setup', 'delivery': 'Delivery'}
        expected = 'Setup\nDelivery'
        self.assertEqual(get_joke(mock_response, 'twopart'), expected)

    def test_get_joke_invalid_type(self):
        mock_response = type('', (), {})()
        mock_response.json = lambda: {'type': 'invalid'}
        with self.assertRaises(ValueError):
            get_joke(mock_response, 'invalid')

    def test_errorhandler(self):
        with self.assertRaises(ValueError):
            error_handler('Exception')

    def test_generate_valid_number_of_jokes(self):  # Should fail, was not able to access logs for specific method
        with requests_mock.Mocker() as rq_mock:
            rq_mock.get(BASE_URL, json={'type': 'single', 'joke': 'A test joke.'})

            # Capture prints to a list - failed, need more time to investigate
            outputs = []
            with self.assertLogs('joke_machine',
                                 level='INFO') as cm:
                joke_machine_runner(3)
                outputs = cm.output

            self.assertEqual(len(outputs), 3)
            self.assertTrue('A test joke.' in outputs[0])

    def test_machine_runner_passes_on_zero(self):
        joke_machine_runner(0)

    def test_machine_runner_fails_on_negative(self):  # Should fail - functionality not implemented yet
        with self.assertRaises(ValueError):
            joke_machine_runner(-1)


if __name__ == '__main__':
    unittest.main()
