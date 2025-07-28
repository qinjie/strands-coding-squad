# API Documentation

This document outlines the API integration with NewsAPI and the internal API structure of the Singapore News Flask application.

## External API: NewsAPI

The application uses [NewsAPI](https://newsapi.org/) to fetch news articles from Singapore.

### Authentication

NewsAPI requires an API key for authentication. The key should be set in the environment variable `NEWS_API_KEY` or in the `.env` file.

### Endpoints Used

#### 1. Top Headlines

**Endpoint:** `GET https://newsapi.org/v2/top-headlines`

**Parameters:**
- `country`: Set to 'sg' for Singapore
- `apiKey`: Your NewsAPI key
- `page`: Page number for pagination (default: 1)
- `pageSize`: Number of results per page (default: 20)
- `category`: Optional category filter (business, entertainment, general, health, science, sports, technology)

**Example Request:**
```
GET https://newsapi.org/v2/top-headlines?country=sg&apiKey=YOUR_API_KEY&page=1&pageSize=20&category=business
```

**Example Response:**
```json
{
  "status": "ok",
  "totalResults": 38,
  "articles": [
    {
      "source": {
        "id": "bbc-news",
        "name": "BBC News"
      },
      "author": "BBC News",
      "title": "Example headline from Singapore",
      "description": "This is an example description of a news article.",
      "url": "https://www.example.com/article",
      "urlToImage": "https://www.example.com/image.jpg",
      "publishedAt": "2025-07-27T12:00:00Z",
      "content": "This is the content of the article..."
    },
    // More articles...
  ]
}
```

#### 2. Search News

**Endpoint:** `GET https://newsapi.org/v2/everything`

**Parameters:**
- `q`: Search query
- `apiKey`: Your NewsAPI key
- `page`: Page number for pagination (default: 1)
- `pageSize`: Number of results per page (default: 20)
- `language`: Language of articles (default: 'en' for English)
- `sortBy`: Sort order (default: 'publishedAt')

**Example Request:**
```
GET https://newsapi.org/v2/everything?q=singapore+finance&apiKey=YOUR_API_KEY&page=1&pageSize=20&language=en&sortBy=publishedAt
```

**Example Response:**
Similar to the Top Headlines response.

### Rate Limits

NewsAPI has the following rate limits:
- Developer plan: 100 requests per day
- Standard plan: 500 requests per day
- Premium plans: Higher limits available

To handle these limits, the application implements caching to reduce the number of API calls.

## Internal API Structure

### API Module (`src/app/api.py`)

The API module provides functions to interact with NewsAPI and handles caching and error management.

#### Functions

##### `get_top_headlines(category=None, page=1)`

Fetches top headlines from Singapore, optionally filtered by category.

**Parameters:**
- `category` (str, optional): News category to filter by
- `page` (int, optional): Page number for pagination

**Returns:**
- dict: JSON response from NewsAPI

**Raises:**
- `NewsAPIException`: If there's an error with the API request

##### `search_news(query, page=1)`

Searches for news articles related to a specific query.

**Parameters:**
- `query` (str): Search query
- `page` (int, optional): Page number for pagination

**Returns:**
- dict: JSON response from NewsAPI

**Raises:**
- `NewsAPIException`: If there's an error with the API request

##### `clear_cache()`

Clears the API cache.

### Error Handling

The API module defines a custom exception `NewsAPIException` for handling API errors. This exception is caught in the routes and displayed to the user with appropriate error messages.

### Caching

The application uses Flask-Caching to cache API responses:

- Cache type: SimpleCache (in-memory) for development, RedisCache for production
- Default timeout: 5 minutes (300 seconds)
- Cache keys are based on function arguments

## Testing the API

You can test the API integration using the provided test suite:

```bash
pytest src/tests/test_api.py
```

## Extending the API

To add support for additional NewsAPI endpoints or features:

1. Add new functions to `src/app/api.py`
2. Implement appropriate caching using the `@cache.memoize()` decorator
3. Handle errors consistently using the `NewsAPIException`
4. Add tests for the new functionality in `src/tests/test_api.py`