# Development Guide

This guide provides instructions for developers working on the Singapore News Flask application.

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- A code editor (VS Code, PyCharm, etc.)
- NewsAPI key (get one at [https://newsapi.org/](https://newsapi.org/))

### Initial Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/project_20250727_singapore_news_flask.git
   cd project_20250727_singapore_news_flask
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**

   Copy the example environment file:
   ```bash
   cp src/config/.env.example src/config/.env
   ```

   Edit the `.env` file and add your NewsAPI key and other configuration options.

6. **Run the application**

   ```bash
   flask run
   ```
   
   Or:
   ```bash
   python run.py
   ```

   The application will be available at [http://localhost:5000](http://localhost:5000).

## Project Structure

```
project_20250727_singapore_news_flask/
├── src/
│   ├── app/
│   │   ├── __init__.py        # Application factory
│   │   ├── routes.py          # Route definitions
│   │   ├── api.py             # NewsAPI integration
│   │   ├── models.py          # Data models
│   │   ├── config.py          # Application configuration
│   │   ├── static/            # Static assets
│   │   └── templates/         # HTML templates
│   ├── tests/                 # Test suite
│   └── config/                # Configuration files
├── docs/                      # Documentation
├── requirements.txt           # Project dependencies
└── run.py                     # Application entry point
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Implement your changes following the coding standards below.

### 3. Run Tests

```bash
pytest
```

For coverage report:
```bash
pytest --cov=src
```

### 4. Format and Lint Your Code

```bash
# Install development tools if not already installed
pip install black flake8 isort

# Format code
black src/

# Sort imports
isort src/

# Lint code
flake8 src/
```

### 5. Commit Changes

```bash
git add .
git commit -m "Add your meaningful commit message here"
```

### 6. Push Changes

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

Create a pull request on GitHub with a clear description of your changes.

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters (Black default)
- Use docstrings for all functions, classes, and modules

### Naming Conventions

- **Variables and Functions**: Use snake_case
- **Classes**: Use PascalCase
- **Constants**: Use UPPER_CASE
- **Private Methods/Variables**: Prefix with underscore (_method_name)

### Code Organization

- Keep functions and methods small and focused
- Follow the Single Responsibility Principle
- Use comments sparingly, prefer self-documenting code
- Group related functionality in modules

## Testing Guidelines

### Test Structure

- Place tests in the `src/tests/` directory
- Name test files with `test_` prefix
- Use descriptive test method names that explain the expected behavior

### Test Coverage

- Aim for at least 80% code coverage
- Test both success and failure cases
- Use mocks for external dependencies (like NewsAPI)

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/test_api.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src
```

## Working with Templates

### Template Structure

- Base template: `base.html` contains the common layout
- Page templates extend the base template
- Use template inheritance for consistent styling

### Template Best Practices

- Keep logic in Python code, not in templates
- Use template macros for reusable components
- Follow proper indentation in HTML templates

## API Integration

### Working with NewsAPI

- All NewsAPI interactions should go through the `api.py` module
- Use caching to reduce API calls
- Handle API errors gracefully
- Test with mock responses

### Adding New API Features

1. Add new methods to `api.py`
2. Implement appropriate caching
3. Add error handling
4. Update tests
5. Document the new functionality

## Debugging

### Flask Debug Mode

Run the application in debug mode during development:

```bash
export FLASK_ENV=development
flask run
```

### Logging

Use the built-in logging module:

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Deployment

### Preparing for Deployment

1. Update dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Set environment variables for production:
   ```bash
   export FLASK_ENV=production
   ```

### Deployment Options

- **Heroku**: Use a Procfile and gunicorn
- **Docker**: Use the provided Dockerfile
- **Traditional Server**: Use gunicorn behind Nginx

## Contributing Guidelines

1. Follow the development workflow outlined above
2. Write clear, concise commit messages
3. Include tests for new features
4. Update documentation as needed
5. Be respectful and constructive in code reviews

## Getting Help

- Check the existing documentation in the `docs/` directory
- Review the codebase for similar implementations
- Ask for help in the project's communication channels

## License

This project is licensed under the MIT License - see the LICENSE file for details.