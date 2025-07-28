import os
from src.app import create_app
from src.config.config import config

# Get configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'default')
app = create_app(config[config_name])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))