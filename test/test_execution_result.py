import unittest
from whipcode import ExecutionResult


class TestExecutionResult(unittest.TestCase):
    def setUp(self):
        self.result = ExecutionResult(
            stdout="Hello, World!",
            stderr="",
            container_age=1.2,
            timeout=False,
            status=200,
            detail="Success",
            rapid={"messages": "Test message"}
        )

    def test_initialization(self):
        self.assertEqual(self.result.stdout, "Hello, World!")
        self.assertEqual(self.result.stderr, "")
        self.assertEqual(self.result.container_age, 1.2)
        self.assertFalse(self.result.timeout)
        self.assertEqual(self.result.status, 200)
        self.assertEqual(self.result.detail, "Success")
        self.assertEqual(self.result.rapid["messages"], "Test message")

    def test_repr(self):
        expected_repr = ("ExecutionResult(status=200, stdout='Hello, World!', "
                         "stderr='', container_age=1.2, timeout=False, detail='Success', "
                         "rapid={'messages': 'Test message'})")
        self.assertEqual(repr(self.result), expected_repr)
