# API Design - Singapore News Flask Application

## Overview

This document outlines the API design for the Singapore News Flask application. It covers both:

1. **External API Integration**: How the application interacts with NewsAPI
2. **Internal API Structure**: How the application's components communicate

## External API Integration: NewsAPI

### NewsAPI Endpoints Used

1. **Top Headlines Endpoint**
   - URL: `https://newsapi.org/v2/top-headlines`
   - Purpose: Fetch breaking news headlines for Singapore
   - Query Parameters:
     - `country=sg` (Singapore)
     - `category` (optional - for filtering by category)
     - `pageSize` (number of results per page)
     - `page` (pagination)
   - Authentication: API Key in header `X-Api-Key`

2. **Everything Endpoint**
   - URL: `https://newsapi.org/v2/everything`
   - Purpose: Search for all articles about Singapore
   - Query Parameters:
     - `q=Singapore` (search query)
     - `sortBy` (relevancy, popularity, publishedAt)
     - `from` (date filter)
     - `to` (date filter)
     - `pageSize` (number of results per page)
     - `page` (pagination)
   - Authentication: API Key in header `X-Api-Key`

### NewsAPI Response Structure

```json
{
  "status": "ok",
  "totalResults": 38,
  "articles": [
    {
      "source": {
        "id": "source-id",
        "name": "Source Name"
      },
      "author": "Author Name",
      "title": "Article Title",
      "description": "Article description",
      "url": "https://article-url.com",
      "urlToImage": "https://image-url.com",
      "publishedAt": "2025-07-26T12:00:00Z",
      "content": "Article content..."
    }
    // More articles...
  ]
}
```

### Rate Limiting Considerations

NewsAPI has the following rate limits:
- Developer plan: 100 requests per day
- Standard plan: 500 requests per day
- Premium plans: Higher limits

Our caching strategy will be designed to work within these constraints while providing a responsive user experience.

## Internal API Structure

### RESTful API Endpoints

#### News Endpoints

1. **Get Latest News**
   - Endpoint: `GET /api/news`
   - Description: Retrieve latest Singapore news
   - Query Parameters:
     - `category` (optional): Filter by news category
     - `page` (optional): Page number for pagination
     - `per_page` (optional): Number of articles per page
   - Response: JSON array of news articles
   - Status Codes:
     - 200: Success
     - 400: Invalid parameters
     - 429: Rate limit exceeded
     - 500: Server error

2. **Get News Categories**
   - Endpoint: `GET /api/categories`
   - Description: Retrieve available news categories
   - Response: JSON array of category objects
   - Status Codes:
     - 200: Success
     - 500: Server error

3. **Get News Article Details**
   - Endpoint: `GET /api/news/{article_id}`
   - Description: Retrieve detailed information about a specific article
   - Path Parameters:
     - `article_id`: Unique identifier for the article
   - Response: JSON object with article details
   - Status Codes:
     - 200: Success
     - 404: Article not found
     - 500: Server error

4. **Search News**
   - Endpoint: `GET /api/news/search`
   - Description: Search for news articles
   - Query Parameters:
     - `q`: Search query
     - `from_date` (optional): Start date for search
     - `to_date` (optional): End date for search
     - `sort_by` (optional): Sort order (relevancy, popularity, publishedAt)
     - `page` (optional): Page number for pagination
     - `per_page` (optional): Number of articles per page
   - Response: JSON array of news articles
   - Status Codes:
     - 200: Success
     - 400: Invalid parameters
     - 429: Rate limit exceeded
     - 500: Server error

#### System Endpoints

1. **Health Check**
   - Endpoint: `GET /api/health`
   - Description: Check system health and API status
   - Response: JSON object with health status
   - Status Codes:
     - 200: System healthy
     - 503: System unhealthy

2. **API Status**
   - Endpoint: `GET /api/status`
   - Description: Get NewsAPI quota and rate limit status
   - Response: JSON object with API status information
   - Status Codes:
     - 200: Success
     - 500: Server error

### Response Formats

#### News Article Object

```json
{
  "id": "unique-article-id",
  "title": "Article Title",
  "description": "Article description",
  "content": "Article content...",
  "source": {
    "id": "source-id",
    "name": "Source Name"
  },
  "author": "Author Name",
  "url": "https://article-url.com",
  "image_url": "https://image-url.com",
  "published_at": "2025-07-26T12:00:00Z",
  "category": "business"
}
```

#### Category Object

```json
{
  "id": "category-id",
  "name": "Category Name",
  "description": "Category description"
}
```

#### Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error details if available
    }
  }
}
```

#### Health Status Response

```json
{
  "status": "healthy",
  "components": {
    "newsapi": {
      "status": "operational",
      "latency": 120
    },
    "cache": {
      "status": "operational",
      "hit_rate": 0.85
    },
    "database": {
      "status": "operational"
    }
  },
  "timestamp": "2025-07-26T12:00:00Z"
}
```

## API Client Implementation

The application will implement a NewsAPI client class that handles:

1. Authentication with the NewsAPI
2. Request formation and parameter validation
3. Response parsing and error handling
4. Rate limit management
5. Caching of responses

```python
# Pseudocode for NewsAPI client
class NewsAPIClient:
    def __init__(self, api_key, cache_manager):
        self.api_key = api_key
        self.cache_manager = cache_manager
        self.base_url = "https://newsapi.org/v2"
        
    def get_top_headlines(self, country="sg", category=None, page=1, page_size=20):
        # Check cache first
        cache_key = f"headlines:{country}:{category}:{page}:{page_size}"
        cached_data = self.cache_manager.get(cache_key)
        
        if cached_data:
            return cached_data
            
        # Make API request if not in cache
        params = {
            "country": country,
            "page": page,
            "pageSize": page_size
        }
        
        if category:
            params["category"] = category
            
        response = self._make_request("/top-headlines", params)
        
        # Cache the response
        self.cache_manager.set(cache_key, response, ttl=300)  # Cache for 5 minutes
        
        return response
        
    def search_news(self, query, from_date=None, to_date=None, sort_by=None, page=1, page_size=20):
        # Similar implementation with caching
        pass
        
    def _make_request(self, endpoint, params):
        # Handle API request, authentication, and error handling
        pass
```

## Caching Strategy

To handle API rate limits efficiently, the application will implement a multi-level caching strategy:

1. **Short-term cache** (5 minutes): For frequently accessed data like top headlines
2. **Medium-term cache** (30 minutes): For search results and category listings
3. **Long-term cache** (24 hours): For article details and historical data
4. **Stale-while-revalidate**: Return cached data while fetching fresh data in the background
5. **Fallback cache**: Use expired cache data when API is unavailable or rate limited

## Error Handling

The API will implement comprehensive error handling:

1. **Input validation**: Validate all parameters before making requests
2. **Rate limit handling**: Detect rate limit errors and use cached data
3. **Timeout handling**: Set appropriate timeouts for external API calls
4. **Circuit breaker pattern**: Temporarily disable API calls after multiple failures
5. **Graceful degradation**: Show partial or cached content when full data is unavailable

## API Documentation

The API will be documented using OpenAPI (Swagger) specification. The documentation will be available at `/api/docs` endpoint and will include:

1. Endpoint descriptions
2. Request parameters
3. Response formats
4. Error codes
5. Example requests and responses

## API Versioning

The API will be versioned to allow for future changes:

1. **URL-based versioning**: `/api/v1/news`
2. **Version header**: `Accept: application/vnd.singapore-news.v1+json`

This allows for backward compatibility as the API evolves.