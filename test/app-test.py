import unittest
from app import app


class HTTPServiceTest(unittest.TestCase):
    def test_base(self):
        # This test is to check the setup.
        self.assertEqual(True, True)

    def test_say_hello(self):
        hello_response = app.say_hello()
        self.assertEqual('Hello', hello_response,
                         f'say_hello() shold have returned "Hello", but it returned "{hello_response}"')


if __name__ == '__main__':
    unittest.main()
