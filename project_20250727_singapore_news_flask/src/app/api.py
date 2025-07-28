import requests
import logging
from flask import current_app
from src.app import cache

logger = logging.getLogger(__name__)

class NewsAPIException(Exception):
    """Custom exception for NewsAPI errors"""
    pass

@cache.memoize(timeout=300)  # Cache for 5 minutes
def get_top_headlines(category=None, page=1):
    """
    Fetch top headlines from NewsAPI for Singapore
    
    Args:
        category (str, optional): News category to filter by
        page (int, optional): Page number for pagination
        
    Returns:
        dict: JSON response from NewsAPI
        
    Raises:
        NewsAPIException: If there's an error with the API request
    """
    api_key = current_app.config['NEWS_API_KEY']
    country = current_app.config['NEWS_COUNTRY']
    page_size = current_app.config['NEWS_PAGE_SIZE']
    
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': country,
        'apiKey': api_key,
        'page': page,
        'pageSize': page_size
    }
    
    if category and category != 'all':
        params['category'] = category
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"NewsAPI request failed: {str(e)}")
        raise NewsAPIException(f"Failed to fetch news: {str(e)}")

@cache.memoize(timeout=300)  # Cache for 5 minutes
def search_news(query, page=1):
    """
    Search for news articles related to a specific query
    
    Args:
        query (str): Search query
        page (int, optional): Page number for pagination
        
    Returns:
        dict: JSON response from NewsAPI
        
    Raises:
        NewsAPIException: If there's an error with the API request
    """
    api_key = current_app.config['NEWS_API_KEY']
    country = current_app.config['NEWS_COUNTRY']
    page_size = current_app.config['NEWS_PAGE_SIZE']
    
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'page': page,
        'pageSize': page_size,
        'language': 'en',  # English language articles
        'sortBy': 'publishedAt'  # Sort by publication date
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"NewsAPI search request failed: {str(e)}")
        raise NewsAPIException(f"Failed to search news: {str(e)}")

def clear_cache():
    """Clear the API cache"""
    cache.clear()