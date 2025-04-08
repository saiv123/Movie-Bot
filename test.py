import unittest
from unittest.mock import patch, MagicMock
from bot import Check, addToWatchList

class TestBotFunctions(unittest.TestCase):

    @patch('secrets.apikey', 'mocked_api_key')  # Mock the apikey from secrets.py
    @patch('bot.requests.get')
    def test_Check_function_success(self, mock_get):
        # Mock the API response for a successful search
        mock_response = {
            "total_results": 1,
            "results": [{"media_type": "movie"}]
        }
        mock_get.return_value.json.return_value = mock_response

        status, json, media_type = Check("Inception")
        self.assertTrue(status)
        self.assertEqual(media_type, "movie")
        self.assertEqual(json, mock_response)

    @patch('secrets.apikey', 'mocked_api_key')  # Mock the apikey from secrets.py
    @patch('bot.requests.get')
    def test_Check_function_no_results(self, mock_get):
        # Mock the API response for no results
        mock_response = {"total_results": 0}
        mock_get.return_value.json.return_value = mock_response

        status, json, media_type = Check("Nonexistent Movie")
        self.assertFalse(status)
        self.assertIsNone(json)
        self.assertIsNone(media_type)

    @patch('secrets.apikey', 'mocked_api_key')  # Mock the apikey from secrets.py
    @patch('bot.requests.post')
    def test_addToWatchList_success(self, mock_post):
        # Mock the API response for a successful watchlist addition
        mock_response = {"success": True}
        mock_post.return_value.json.return_value = mock_response

        result = addToWatchList(12345, "movie")
        self.assertTrue(result)

    @patch('secrets.apikey', 'mocked_api_key')  # Mock the apikey from secrets.py
    @patch('bot.requests.post')
    def test_addToWatchList_failure(self, mock_post):
        # Mock the API response for a failed watchlist addition
        mock_response = {"success": False}
        mock_post.return_value.json.return_value = mock_response

        result = addToWatchList(12345, "movie")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()