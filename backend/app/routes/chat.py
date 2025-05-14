import sys
import os
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.utils.utils import error_response, success_response
from app.services.ai_providers.provider_registry import ProviderRegistry
from app.services.model_discovery import ModelDiscoveryService
import base64
import json
import logging
from io import BytesIO

chat_bp = Blueprint('chat', __name__)
provider_registry = ProviderRegistry()
model_discovery = ModelDiscoveryService(provider_registry)
logger = logging.getLogger(__name__)

@chat_bp.route('/providers', methods=['GET'])
def list_providers():
    """List all available providers"""
    return success_response({
        "providers": [
            {"id": pid, "name": pid.capitalize()} for pid in provider_registry.get_available_provider_ids()
        ]
    })

@chat_bp.route('/providers/<provider_id>/models', methods=['GET'])
def list_models(provider_id):
    """List available models for the given provider"""
    refresh = request.args.get('refresh', 'false').lower() == 'true'
    if refresh:
        model_discovery.refresh_models(provider_id)
    models = model_discovery.get_available_models(provider_id)
    return success_response({"models": models})

@chat_bp.route('/chat/completions', methods=['POST'])
def generate_completion():
    """Generate a chat completion"""
    data = request.json
    provider_id = data.get('provider')
    model = data.get('model')
    messages = data.get('messages', [])
    options = data.get('options', {})
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        return error_response("Provider not configured")
    response = provider.generate_completion(messages, model, options)
    if isinstance(response, dict) and response.get("error"):
        return error_response(response["error"])
    return success_response(response)

@chat_bp.route('/chat/stream', methods=['POST'])
def stream_completion():
    """Generate a streaming chat completion"""
    data = request.json
    provider_id = data.get('provider')
    model = data.get('model')
    messages = data.get('messages', [])
    options = data.get('options', {})
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        return error_response("Provider not configured")

    def generate():
        try:
            for chunk in provider.stream_completion(messages, model, options):
                yield chunk
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield f"Error: {str(e)}"

    return Response(stream_with_context(generate()), content_type='text/plain')

@chat_bp.route('/chat/upload', methods=['POST'])
def upload_file():
    """Process an uploaded file for chat context"""
    if 'file' not in request.files:
        return error_response("No file provided")
    file = request.files['file']
    provider_id = request.form.get('provider')
    model = request.form.get('model')
    prompt = request.form.get('prompt', 'Analyze this file and provide insights.')
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        return error_response("Provider not configured")
    
    try:
        # Read file content
        file_content = file.read()
        file_type = file.content_type or 'application/octet-stream'
        file_name = file.filename
        
        # Process file based on type (simplified, to be expanded with actual processing)
        if file_type.startswith('image/'):
            content = base64.b64encode(file_content).decode('utf-8')
            response = provider.process_image(content, prompt, model)
        elif file_type in ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            # Placeholder for document processing
            response = {"content": f"Processed file {file_name} with prompt: {prompt}"}
        else:
            return error_response(f"Unsupported file type: {file_type}")
        
        if isinstance(response, dict) and response.get("error"):
            return error_response(response["error"])
        return success_response(response)
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return error_response(str(e))

@chat_bp.route('/chat/image', methods=['POST'])
def process_image():
    """Process an image with the given prompt"""
    if 'image' not in request.files:
        return error_response("No image provided")
    image_file = request.files['image']
    image_data = base64.b64encode(image_file.read()).decode('utf-8')
    provider_id = request.form.get('provider')
    model = request.form.get('model')
    prompt = request.form.get('prompt', '')
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        return error_response("Provider not configured")
    response = provider.process_image(image_data, prompt, model)
    return success_response(response)

@chat_bp.route('/providers/register', methods=['POST'])
def register_provider():
    """Register a provider with an API key"""
    data = request.json
    provider_id = data.get('provider_id')
    api_key = data.get('api_key')
    if not provider_id or not api_key:
        return error_response("provider_id and api_key are required")
    try:
        provider_registry.register_provider(provider_id, api_key)
        return success_response({"success": True, "provider_id": provider_id})
    except Exception as e:
        return error_response(str(e))
