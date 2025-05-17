import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'

    # Logging configuration
    LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Default Provider Configuration
    DEFAULT_PROVIDER = os.getenv('DEFAULT_PROVIDER', 'deepseek')
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'deepseek-chat')

    # Provider API Keys
    PROVIDER_KEYS = {
        'openai': os.getenv('OPENAI_API_KEY'),
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'google': os.getenv('GOOGLE_AI_API_KEY'),
        'deepseek': os.getenv('DEEPSEEK_API_KEY'),
        'groq': os.getenv('GROQ_API_KEY'),
        'mistral': os.getenv('MISTRAL_API_KEY'),
        'cohere': os.getenv('COHERE_API_KEY'),
        'gemini': os.getenv('GEMINI_API_KEY'),
        'alibaba': os.getenv('ALIBABA_API_KEY'),
        'openrouterai': os.getenv('OPENROUTERAI_API_KEY'),
        'huggingface': os.getenv('HUGGINGFACE_API_KEY')
    }

def configure_logging(app):
    """Configure logging for the application"""
    # Remove default handlers
    del app.logger.handlers[:]
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOGGING_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(Config.LOGGING_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handler to app logger
    app.logger.addHandler(console_handler)
    app.logger.setLevel(Config.LOGGING_LEVEL)

    # Log startup information
    app.logger.info(f"Application started in {'Development' if Config.DEBUG else 'Production'} mode")
    
    # Log available providers
    available_providers = [
        provider for provider, key in Config.PROVIDER_KEYS.items() if key
    ]
    app.logger.info(f"Available Providers: {', '.join(available_providers)}")
    
    # Log default provider and model
    app.logger.info(f"Default Provider: {Config.DEFAULT_PROVIDER}")
    app.logger.info(f"Default Model: {Config.DEFAULT_MODEL}")
