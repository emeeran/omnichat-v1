from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def add_root_route(app):
    @app.route("/")
    def root():
        return {"message": "AI Assistant backend is running."}

def create_app(config_name=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure the app
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    if config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    elif config_name == 'production':
        app.config.from_object('app.config.ProductionConfig')
    
    # Register root route
    add_root_route(app)
    
    # Import and register blueprints
    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    # Additional setup can go here (database, logging, etc.)
    
    return app
