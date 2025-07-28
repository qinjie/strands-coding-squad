import unittest
from flask import url_for
from src.app import create_app
from src.config.config import TestingConfig
import json
from unittest.mock import patch

class TestApp(unittest.TestCase):
    """Test cases for the Flask application"""
    
    def setUp(self):
        """Set up test client and app context"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
        
    def test_index_page(self):
        """Test the index page loads correctly"""
        with patch('src.app.api.get_top_headlines') as mock_get_headlines:
            # Mock API response
            mock_get_headlines.return_value = {
                'status': 'ok',
                'totalResults': 2,
                'articles': [
                    {
                        'source': {'id': 'test-source', 'name': 'Test Source'},
                        'author': 'Test Author',
                        'title': 'Test Title 1',
                        'description': 'Test Description 1',
                        'url': 'https://example.com/1',
                        'urlToImage': 'https://example.com/image1.jpg',
                        'publishedAt': '2025-07-27T12:00:00Z',
                        'content': 'Test content 1'
                    },
                    {
                        'source': {'id': 'test-source-2', 'name': 'Test Source 2'},
                        'author': 'Test Author 2',
                        'title': 'Test Title 2',
                        'description': 'Test Description 2',
                        'url': 'https://example.com/2',
                        'urlToImage': 'https://example.com/image2.jpg',
                        'publishedAt': '2025-07-27T13:00:00Z',
                        'content': 'Test content 2'
                    }
                ]
            }
            
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Latest News in Singapore', response.data)
            self.assertIn(b'Test Title 1', response.data)
            self.assertIn(b'Test Title 2', response.data)
            
    def test_category_page(self):
        """Test category filtering works correctly"""
        with patch('src.app.api.get_top_headlines') as mock_get_headlines:
            # Mock API response
            mock_get_headlines.return_value = {
                'status': 'ok',
                'totalResults': 1,
                'articles': [
                    {
                        'source': {'id': 'test-source', 'name': 'Test Source'},
                        'author': 'Test Author',
                        'title': 'Test Business Title',
                        'description': 'Test Business Description',
                        'url': 'https://example.com/business',
                        'urlToImage': 'https://example.com/business.jpg',
                        'publishedAt': '2025-07-27T12:00:00Z',
                        'content': 'Test business content'
                    }
                ]
            }
            
            response = self.client.get('/category/business')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Business News', response.data)
            self.assertIn(b'Test Business Title', response.data)
            
    def test_search_page(self):
        """Test search functionality works correctly"""
        with patch('src.app.api.search_news') as mock_search_news:
            # Mock API response
            mock_search_news.return_value = {
                'status': 'ok',
                'totalResults': 1,
                'articles': [
                    {
                        'source': {'id': 'test-source', 'name': 'Test Source'},
                        'author': 'Test Author',
                        'title': 'Test Search Result',
                        'description': 'Test Search Description',
                        'url': 'https://example.com/search',
                        'urlToImage': 'https://example.com/search.jpg',
                        'publishedAt': '2025-07-27T12:00:00Z',
                        'content': 'Test search content'
                    }
                ]
            }
            
            response = self.client.get('/search?q=test')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Search Results', response.data)
            self.assertIn(b'test', response.data)
            self.assertIn(b'Test Search Result', response.data)
            
    def test_article_page(self):
        """Test article detail page works correctly"""
        article_params = {
            'title': 'Test Article Title',
            'url': 'https://example.com/article',
            'source_name': 'Test Source',
            'author': 'Test Author',
            'description': 'Test Article Description',
            'url_to_image': 'https://example.com/article.jpg',
            'published_at': '2025-07-27T12:00:00Z',
            'content': 'Test article content'
        }
        
        response = self.client.get('/article', query_string=article_params)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Article Title', response.data)
        self.assertIn(b'Test Source', response.data)
        self.assertIn(b'Test Author', response.data)
        self.assertIn(b'Test Article Description', response.data)
        
    def test_error_page(self):
        """Test 404 error page works correctly"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Oops! Something went wrong', response.data)
        
if __name__ == '__main__':
    unittest.main()