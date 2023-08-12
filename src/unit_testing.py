import unittest
from unittest.mock import MagicMock, patch
from utils import (get_series_by_date, save_to_json,
                   get_series_for_december_2022, normalized_json)

class TestMyModule(unittest.TestCase):

    def test_get_series_by_date_success(self):
        with patch('utils.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [{'id': 1, 'name': 'Series 1'}]
            mock_get.return_value = mock_response

            result = get_series_by_date('2022-12-01')

            self.assertEqual(result, [{'id': 1, 'name': 'Series 1'}])

    def test_get_series_by_date_failure(self):
        with patch('utils.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = get_series_by_date('2022-12-01')

            self.assertIsNone(result)

    def test_get_series_for_december_2022(self):
        with patch('utils.get_series_by_date') as mock_get_series_by_date:
            mock_get_series_by_date.side_effect = [
                [{'id': 1, 'name': 'Series 1'}],
                [{'id': 2, 'name': 'Series 2'}],
            ]

            result = get_series_for_december_2022()

            self.assertEqual(result, [{'id': 1, 'name': 'Series 1'}, {'id': 2, 'name': 'Series 2'}])

    def test_normalized_json(self):
        json_list = [
            {
                "id": 2450906,
                "name": "\u0421\u0435\u0440\u0438\u044f 87",
                "_embedded": {
                    "show": {
                        "id": 55724,
                        "name": "\u0425\u043e\u0447\u0443 \u0432\u0441\u0435 \u0437\u043d\u0430\u0442\u044c!"
                    }
                }
            }
        ]

        result = normalized_json(json_list)


if __name__ == '__main__':
    unittest.main()
