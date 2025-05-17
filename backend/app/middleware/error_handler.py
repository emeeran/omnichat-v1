from functools import wraps
from flask import jsonify, current_app

def handle_provider_errors(func):
    """
    Decorator to handle errors in provider-related routes
    Provides consistent error response format
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            # Validation errors (e.g., invalid provider ID)
            current_app.logger.warning(f"Validation Error: {ve}")
            return jsonify({
                'error': 'Validation Error',
                'message': str(ve)
            }), 400
        except KeyError as ke:
            # Missing required keys
            current_app.logger.warning(f"Missing Key Error: {ke}")
            return jsonify({
                'error': 'Missing Required Information',
                'message': str(ke)
            }), 400
        except Exception as e:
            # Unexpected errors
            current_app.logger.error(f"Unexpected Provider Error: {e}")
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred while processing your request'
            }), 500
    return wrapper
