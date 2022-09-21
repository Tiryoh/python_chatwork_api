from chatwork.base import ChatworkAPI
from chatwork.base import ChatworkError

import requests
import unittest
from unittest import mock

# ref: https://tubuyaki-tech.hatenablog.com/entry/2021/04/15/073000

api = ChatworkAPI(api_key="apiapi")


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.status_code = status_code
            self.json_data = json_data
            self.text = None

        def raise_for_status(self):
            response = requests.Response()
            response.status_code = self.status_code
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise e

        def json(self):
            return self.json_data

    # if args[0] == "GET" and kwargs["uri"] == "url_valid":
    if args[0] == api.base_url + "url_valid" and \
            kwargs["headers"]["x-chatworktoken"] == "apiapi":
        return MockResponse({"key1": "value1"}, 200)

    # if kwargs['headers']['Authorization'] == 'Bearer valid':
    #     return MockResponse({"key1": "value1"}, 200)

    return MockResponse({"status": "null"}, 404)


# テスト用クラス
class TestGetResp(unittest.TestCase):

    # 正常系確認テストケース
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_resp_ok(self, mock_get):
        res = api.invoke_method("GET", uri="url_valid")

        expected_res = {"key1": "value1"}

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), expected_res)

    # 異常系確認テストケース
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_resp_ng(self, mock_get):
        with self.assertRaises(ChatworkError):
            res = api.invoke_method("GET", uri="url_invalid")


if __name__ == '__main__':
    unittest.main()
