import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-singapore-news-app'
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'your-news-api-key'
    CACHE_TYPE = 'SimpleCache'  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes cache timeout
    NEWS_COUNTRY = 'sg'  # Singapore country code for NewsAPI
    NEWS_PAGE_SIZE = 20  # Number of articles per page
    NEWS_CATEGORIES = [
        'general', 'business', 'entertainment', 'health', 
        'science', 'sports', 'technology'
    ]