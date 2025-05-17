from flask import Blueprint, jsonify, request
from app.services.model_discovery import ModelDiscoveryService
from app.services.ai_providers.provider_registry import ProviderRegistry
from app.middleware.error_handler import handle_provider_errors
import logging
from app.services.ai_providers.models import get_models_for_provider
from app.services.ai_providers.registry_singleton import provider_registry

providers_bp = Blueprint('providers', __name__)
model_discovery = ModelDiscoveryService()
logger = logging.getLogger(__name__)

@providers_bp.route('/providers', methods=['GET'])
@handle_provider_errors
def get_providers():
    """
    Get a list of all available providers
    """
    providers = [
        {"id": pid, "name": pid.capitalize()}
        for pid in provider_registry.get_available_provider_ids()
    ]
    return jsonify(providers), 200

@providers_bp.route('/models/<provider_id>', methods=['GET'])
@handle_provider_errors
def get_models(provider_id):
    """
    Get supported models for a specific provider
    """
    # First try to fetch latest models
    models = model_discovery.fetch_latest_models(provider_id)
    logger.info(f"Fetched latest models for {provider_id}: {models}")
    
    # If no models found, try cached models
    if not models:
        models = model_discovery.get_supported_models(provider_id)
        logger.info(f"Cached models for {provider_id}: {models}")
    
    # If still no models, try static models from models.py
    if not models:
        models = get_models_for_provider(provider_id)
        logger.info(f"Static models for {provider_id}: {models}")
    
    # If still no models, return an error
    if not models:
        logger.warning(f"No models found for provider: {provider_id}")
        return jsonify({
            "error": f"No models available for provider {provider_id}",
            "available_providers": list(provider_registry.get_available_provider_ids())
        }), 404
    
    return jsonify(models), 200

@providers_bp.route('/providers/register', methods=['POST'])
@handle_provider_errors
def register_provider():
    """
    Register a provider with an API key
    """
    data = request.get_json()
    
    # Validate input
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    provider_id = data.get('provider_id')
    api_key = data.get('api_key')
    
    # Validate provider and API key
    if not provider_id:
        return jsonify({"error": "Provider ID is required"}), 400
    if not api_key:
        return jsonify({"error": "API key is required"}), 400
    
    # Attempt to register provider
    try:
        provider = provider_registry.register_provider(provider_id, api_key)
        return jsonify({
            "success": True,
            "message": f"{provider_id.capitalize()} provider registered successfully",
            "provider": str(provider)
        }), 200
    except ValueError as ve:
        logger.warning(f"Provider registration failed: {ve}")
        return jsonify({
            "error": str(ve),
            "available_providers": list(provider_registry.get_available_provider_ids())
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error registering provider: {e}")
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

@providers_bp.route('/providers/default', methods=['GET'])
@handle_provider_errors
def get_default_provider():
    """
    Get the default provider configuration
    """
    default_provider = provider_registry.get_default_provider()
    default_model = provider_registry.get_default_model()
    
    return jsonify({
        "provider": default_provider.name if default_provider else "deepseek",
        "model": default_model
    }), 200
