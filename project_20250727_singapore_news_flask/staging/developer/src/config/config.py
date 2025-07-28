import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BaseConfig:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-singapore-news-app'
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes cache timeout
    NEWS_COUNTRY = 'sg'  # Singapore country code for NewsAPI
    NEWS_PAGE_SIZE = 20  # Number of articles per page
    NEWS_CATEGORIES = [
        'general', 'business', 'entertainment', 'health', 
        'science', 'sports', 'technology'
    ]
    
class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    # Use a faster cache for testing
    CACHE_TYPE = 'NullCache'
    
class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Use Redis cache in production for better performance
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes cache timeout

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}