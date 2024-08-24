import unittest
import json
from app import app

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the test client
        cls.client = app.test_client()
        cls.client.testing = True

    def test_get_system_info(self):
        # Test the '/' route
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('public_ip', data)
        self.assertIn('hostname', data)
        self.assertIn('local_ip', data)
        self.assertIn('os_info', data)

    def test_echo_message(self):
        # Test the '/echo' route with a message
        message = 'Hello, World!'
        response = self.client.get(f'/echo?message={message}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], message)

        # Test the '/echo' route without a message
        response = self.client.get('/echo')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'No message provided')

    def test_status(self):
        # Test the '/status' route
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['message'], 'Application is running')

    def test_logging(self):
        # Test that logging is working by triggering a request and checking the log file
        with open('app.log', 'r') as f:
            pre_log_lines = f.readlines()

        # Trigger a request
        self.client.get('/')

        with open('app.log', 'r') as f:
            post_log_lines = f.readlines()

        # Ensure that a new log line was added
        self.assertTrue(len(post_log_lines) > len(pre_log_lines))

    def test_invalid_route(self):
        # Test a route that doesn't exist
        response = self.client.get('/invalid')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
