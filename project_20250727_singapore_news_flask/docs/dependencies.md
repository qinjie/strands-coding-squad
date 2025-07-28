# Dependencies

This document outlines all dependencies used in the Singapore News Flask application.

## Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework for building the application |
| Flask-Caching | 2.1.0 | Extension for adding caching support to Flask |
| python-dotenv | 1.0.0 | Loading environment variables from .env files |
| requests | 2.31.0 | HTTP library for making API requests |
| Werkzeug | 2.3.7 | WSGI web application library used by Flask |

## Testing Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.0 | Testing framework |
| pytest-cov | 4.1.0 | Coverage reporting for tests |

## Production Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| gunicorn | 21.2.0 | WSGI HTTP server for deploying in production |
| redis | 5.0.0 | Redis client for caching in production |

## Frontend Dependencies (CDN)

| Library | Version | Purpose |
|---------|---------|---------|
| Bootstrap | 5.3.0 | CSS framework for responsive design |
| Font Awesome | 6.4.0 | Icon library |

## System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API calls to NewsAPI)
- Redis (optional, for production caching)

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Dependency Management

### Adding new dependencies

When adding new dependencies to the project:

1. Install the package:
   ```bash
   pip install package-name
   ```

2. Add it to requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```
   
   Or manually add it with the specific version:
   ```
   package-name==1.0.0
   ```

### Updating dependencies

To update all dependencies to their latest versions:

```bash
pip install --upgrade -r requirements.txt
```

To update a specific package:

```bash
pip install --upgrade package-name
```

Then update the requirements.txt file:

```bash
pip freeze > requirements.txt
```

## Dependency Conflicts

If you encounter dependency conflicts, consider using a tool like `pip-tools` to resolve them:

```bash
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

## Security Considerations

- Dependencies are regularly scanned for security vulnerabilities
- Production deployments should use pinned dependency versions to ensure consistency
- Consider using tools like `safety` or `pip-audit` to check for known vulnerabilities:
  ```bash
  pip install safety
  safety check -r requirements.txt
  ```