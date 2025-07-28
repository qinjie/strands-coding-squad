import unittest
from unittest.mock import patch, MagicMock
from src.app import create_app
from src.app.api import get_top_headlines, search_news, NewsAPIException
from src.config.config import TestingConfig
import requests

class TestAPI(unittest.TestCase):
    """Test cases for the API module"""
    
    def setUp(self):
        """Set up test client and app context"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
        
    @patch('src.app.api.requests.get')
    def test_get_top_headlines_success(self, mock_get):
        """Test successful API call to get top headlines"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ok',
            'totalResults': 2,
            'articles': [
                {
                    'source': {'id': 'test-source', 'name': 'Test Source'},
                    'title': 'Test Title 1'
                },
                {
                    'source': {'id': 'test-source-2', 'name': 'Test Source 2'},
                    'title': 'Test Title 2'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_top_headlines()
        
        # Assertions
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['totalResults'], 2)
        self.assertEqual(len(result['articles']), 2)
        self.assertEqual(result['articles'][0]['title'], 'Test Title 1')
        
        # Verify the API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://newsapi.org/v2/top-headlines')
        self.assertEqual(kwargs['params']['country'], 'sg')
        
    @patch('src.app.api.requests.get')
    def test_get_top_headlines_with_category(self, mock_get):
        """Test API call with category filter"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ok',
            'totalResults': 1,
            'articles': [
                {
                    'source': {'id': 'test-source', 'name': 'Test Source'},
                    'title': 'Test Business Title'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the function with category
        result = get_top_headlines(category='business')
        
        # Assertions
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['totalResults'], 1)
        
        # Verify the API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['category'], 'business')
        
    @patch('src.app.api.requests.get')
    def test_get_top_headlines_api_error(self, mock_get):
        """Test handling of API errors"""
        # Mock a failed response
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        # Call the function and check for exception
        with self.assertRaises(NewsAPIException):
            get_top_headlines()
            
    @patch('src.app.api.requests.get')
    def test_search_news_success(self, mock_get):
        """Test successful API call to search news"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ok',
            'totalResults': 1,
            'articles': [
                {
                    'source': {'id': 'test-source', 'name': 'Test Source'},
                    'title': 'Test Search Result'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the function
        result = search_news('test query')
        
        # Assertions
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['totalResults'], 1)
        self.assertEqual(result['articles'][0]['title'], 'Test Search Result')
        
        # Verify the API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://newsapi.org/v2/everything')
        self.assertEqual(kwargs['params']['q'], 'test query')
        
    @patch('src.app.api.requests.get')
    def test_search_news_api_error(self, mock_get):
        """Test handling of API errors in search"""
        # Mock a failed response
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        # Call the function and check for exception
        with self.assertRaises(NewsAPIException):
            search_news('test query')
            
if __name__ == '__main__':
    unittest.main()