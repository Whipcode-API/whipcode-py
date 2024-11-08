import unittest
from unittest.mock import patch, AsyncMock
import asyncio

from whipcode import Whipcode
from whipcode.exceptions import RequestError


class TestWhipcodeAsyncClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = Whipcode()
        self.client.rapid_key("test-key")

    @patch("aiohttp.ClientSession.post")
    async def test_run_async(self, mock_post):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "stdout": "async output",
            "stderr": "",
            "container_age": 1.0,
            "timeout": False,
            "detail": "async success"
        }
        mock_post.return_value.__aenter__.return_value = mock_response
        future = self.client.run_async("print('Hello')", language_id=1)
        result = await future
        self.assertEqual(result.status, 200)
        self.assertEqual(result.stdout, "async output")
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.container_age, 1.0)
        self.assertFalse(result.timeout)
        self.assertEqual(result.detail, "async success")

    @patch("aiohttp.ClientSession.post")
    async def test_run_async_request_error(self, mock_post):
        mock_post.side_effect = Exception("Async network error")
        with self.assertRaises(RequestError):
            future = self.client.run_async("print('Hello')", language_id=1)
            await future
