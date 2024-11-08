import unittest
from unittest.mock import patch, MagicMock

from whipcode import Whipcode
from whipcode.exceptions import RequestError, PayloadBuildError


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Whipcode()
        self.client.rapid_key("test-key")

    def test_rapid_key(self):
        self.client.rapid_key("new-key")
        self.assertEqual(self.client.provider["headers"]["X-RapidAPI-Key"], "new-key")

    def test_build_payload(self):
        payload = self.client._build_payload(
            code="print('Hello, World!')",
            language_id=1,
            args=["arg1", "arg2"],
            timeout=5
        )
        expected_payload = {
            "code": "cHJpbnQoJ0hlbGxvLCBXb3JsZCEnKQ==",
            "language_id": "1",
            "args": "arg1 arg2",
            "timeout": 5
        }
        self.assertEqual(payload, expected_payload)

    def test_build_payload_error(self):
        with self.assertRaises(PayloadBuildError):
            self.client._build_payload(code=None, language_id=1, args=[], timeout=5)

    @patch("requests.post")
    def test_run(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "stdout": "output",
            "stderr": "",
            "container_age": 0.5,
            "timeout": False,
            "detail": "success"
        }
        mock_post.return_value = mock_response
        result = self.client.run("print('Hello')", language_id=1)
        self.assertEqual(result.status, 200)
        self.assertEqual(result.stdout, "output")
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.container_age, 0.5)
        self.assertFalse(result.timeout)
        self.assertEqual(result.detail, "success")

    @patch("requests.post")
    def test_request_error(self, mock_post):
        mock_post.side_effect = Exception("Network error")
        with self.assertRaises(RequestError):
            self.client.run("print('Hello')", language_id=1)
