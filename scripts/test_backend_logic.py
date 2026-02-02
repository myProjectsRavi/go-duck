import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.index import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_no_query(self):
        response = self.client.get('/api/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No query provided', response.get_json()['error'])

    @patch('api.index.DDGS')
    @patch('api.index.trafilatura')
    def test_search_success(self, mock_trafilatura, mock_ddgs):
        # Mock DDGS results
        mock_ddgs_instance = mock_ddgs.return_value
        # ddgs.text() returns an iterable.
        mock_ddgs_instance.text.return_value = [
            {'title': 'Test News', 'href': 'http://test.com', 'body': 'This is a test snippet.'}
        ]

        # Mock Trafilatura
        mock_trafilatura.fetch_url.return_value = "<html><body>Some content about revenue surge.</body></html>"
        mock_trafilatura.extract.return_value = "Some content about revenue surge. It is a good day."

        response = self.client.get('/api/search?q=Test')
        if response.status_code != 200:
            print(response.get_json())

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['headline'], 'Test News')

        # Check sentiment structure
        self.assertIn('sentiment', data['results'][0])
        self.assertIn('score', data['results'][0]['sentiment'])
        self.assertIn('label', data['results'][0]['sentiment'])

if __name__ == '__main__':
    unittest.main()
