from flask import Flask
from flask_cors import CORS
from .routes.chat import chat_bp
from .routes.providers import providers_bp
from .config import Config, configure_logging
from .services.monitoring import MonitoringService
from app.services.ai_providers.registry_singleton import provider_registry

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Apply configuration
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configure logging
    configure_logging(app)

    # Initialize monitoring service - commented out to avoid port conflict
    monitoring_service = MonitoringService()
    # monitoring_service.start_server()

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(providers_bp, url_prefix='/api')

    # --- Auto-register providers with API keys from .env ---
    # (Now handled in registry_singleton.py)
    # --- End auto-registration ---

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'Not Found: {error}')
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return {'error': 'Internal server error'}, 500

    return app
