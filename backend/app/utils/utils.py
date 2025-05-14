"""
utils.py - Common backend utility functions for error handling and response formatting
"""
from flask import jsonify

def error_response(message, status=400):
    """Return a standardized error response."""
    return jsonify({"error": message}), status

def success_response(data, status=200):
    """Return a standardized success response."""
    return jsonify(data), status
