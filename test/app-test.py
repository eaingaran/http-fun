import unittest
from app.app import app
import json
import git


class HTTPServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_base(self):
        # This test is to check the setup.
        self.assertEqual(True, True)

    def test_greeting(self):
        with app.test_client() as client:
            response = client.get('/helloworld')
            self.assertEqual(200, response.status_code)
            self.assertEqual('Hello Stranger', response.data.decode('ascii'))

    def test_greeting_with_name(self):
        with app.test_client() as client:
            response = client.get('/helloworld?name=Aingaran')
            self.assertEqual(200, response.status_code)
            self.assertEqual('Hello Aingaran', response.data.decode('ascii'))

            response = client.get('/helloworld?name=AingaranElango')
            self.assertEqual(200, response.status_code)
            self.assertEqual('Hello Aingaran Elango', response.data.decode('ascii'))

            response = client.get('/helloworld?name=AlfredENeumann')
            self.assertEqual(200, response.status_code)
            self.assertEqual('Hello Alfred E Neumann', response.data.decode('ascii'))

            response = client.get('/helloworld?name=')
            self.assertEqual(200, response.status_code)
            self.assertEqual('Hello ', response.data.decode('ascii'))

    def test_versions(self):
        with app.test_client() as client:
            response = client.get('/versionz')
            self.assertEqual(200, response.status_code)
            payload = json.loads(response.data.decode('ascii'))
            self.assertIsNotNone(payload)
            repo = git.Repo(search_parent_directories=True)
            self.assertEqual(repo.head.object.hexsha, payload['git hash'])
            self.assertEqual(repo.remotes.origin.url.split('.git')[0].split('/')[-1], payload['name'])

    def test_404(self):
        with app.test_client() as client:
            response = client.get('/random')
            self.assertEqual(404, response.status_code)
            payload = json.loads(response.data.decode('ascii'))
            self.assertIsNotNone(payload)
            self.assertEqual(404, payload['Status Code'])
            self.assertEqual("404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", payload['Message'])


if __name__ == '__main__':
    unittest.main()
