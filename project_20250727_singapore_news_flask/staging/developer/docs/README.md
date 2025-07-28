# Singapore News Flask Application

A Flask web application that displays the latest news in Singapore using the NewsAPI.

## Features

- Display latest news articles from Singapore in a card format
- Filter news by categories (general, business, entertainment, health, science, sports, technology)
- View detailed information about individual articles
- Search for specific news articles
- Responsive design for both desktop and mobile devices
- Caching to handle API rate limits
- Error handling for API failures

## Screenshots

*[Screenshots would be added here in a real project]*

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- NewsAPI key (get one at [https://newsapi.org/](https://newsapi.org/))

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/project_20250727_singapore_news_flask.git
   cd project_20250727_singapore_news_flask
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp src/config/.env.example src/config/.env
   ```
   
   Edit the `.env` file and add your NewsAPI key and other configuration options.

## Usage

### Development Server

Run the development server:
```
flask run
```
or
```
python run.py
```

The application will be available at [http://localhost:5000](http://localhost:5000).

### Production Deployment

For production deployment, it's recommended to use Gunicorn:
```
gunicorn -w 4 "run:app"
```

## Configuration

The application can be configured using environment variables:

- `FLASK_ENV`: Set to `development`, `testing`, or `production` (default: `development`)
- `SECRET_KEY`: Secret key for Flask session security
- `NEWS_API_KEY`: Your NewsAPI key
- `REDIS_URL`: Redis URL for caching in production (optional)

See `src/config/config.py` for more configuration options.

## Testing

Run the tests:
```
pytest
```

Run tests with coverage:
```
pytest --cov=src
```

## Project Structure

```
project_20250727_singapore_news_flask/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── api.py
│   │   ├── models.py
│   │   ├── config.py
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── img/
│   │   └── templates/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── article.html
│   │       └── error.html
│   ├── tests/
│   │   ├── test_app.py
│   │   └── test_api.py
│   └── config/
│       ├── config.py
│       └── .env.example
├── docs/
│   ├── README.md
│   ├── dependencies.md
│   ├── api/
│   │   └── api_documentation.md
│   ├── implementation_notes.md
│   ├── performance_guide.md
│   ├── security_implementation.md
│   └── development_guide.md
├── requirements.txt
└── run.py
```

## License

[MIT License](LICENSE)

## Acknowledgements

- [NewsAPI](https://newsapi.org/) for providing the news data
- [Flask](https://flask.palletsprojects.com/) web framework
- [Bootstrap](https://getbootstrap.com/) for responsive design