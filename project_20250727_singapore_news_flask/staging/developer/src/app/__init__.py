from flask import Flask
from flask_caching import Cache
from src.app.config import Config

# Initialize cache
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    cache.init_app(app)
    
    # Register blueprints
    from src.app.routes import main
    app.register_blueprint(main)
    
    return app