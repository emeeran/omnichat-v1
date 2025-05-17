"""
Models definition for various AI providers.
This file contains a structured dictionary of providers and their associated models.
"""

from app.config import Config
from .provider_registry import ProviderRegistry

# Initialize provider registry to access available providers
provider_registry = ProviderRegistry()

# Define a dictionary of providers and their models
# This can be used as a fallback or for quick reference
PROVIDER_MODELS = {
    "openai": [
        "gpt-4o-realtime-preview-2024-12-17",
        "gpt-4o-audio-preview-2024-12-17",
        "gpt-4o-audio-preview-2024-10-01",
        "gpt-4o-mini-audio-preview",
        "gpt-4o-audio-preview",
        "gpt-4o-mini-realtime-preview",
        "gpt-4o-mini-realtime-preview-2024-12-17",
        "gpt-4.1-nano",
        "gpt-4o-mini-search-preview",
        "gpt-4.1-nano-2025-04-14",
        "gpt-4o-realtime-preview",
        "gpt-4o-search-preview",
        "gpt-4o-mini-search-preview-2025-03-11",
        "gpt-4-0125-preview",
        "gpt-4o-2024-11-20",
        "gpt-4o-2024-05-13",
        "gpt-4o-mini-tts",
        "gpt-4o-transcribe",
        "gpt-4.5-preview",
        "gpt-4.5-preview-2025-02-27",
        "gpt-4o-search-preview-2025-03-11",
        "gpt-image-1",
        "gpt-4o",
        "gpt-4o-2024-08-06",
        "gpt-4o-mini-2024-07-18",
        "gpt-4.1-mini",
        "gpt-4o-mini",
        "gpt-4o-mini-audio-preview-2024-12-17",
        "gpt-4o-realtime-preview-2024-10-01",
        "gpt-4o-mini-transcribe",
        "gpt-4.1-mini-2025-04-14",
        "gpt-4.1",
        "gpt-4.1-2025-04-14"
    ],
    "anthropic": [
        "claude-3-5-sonnet-20241022",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229"
    ],
    "groq": [
        "distil-whisper-large-v3-en",
        "gemma2-9b-it",
        "gemma-7b-it-deprecated",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-guard-3-8b",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "whisper-large-v3",
        "whisper-large-v3-turbo"
    ],
    "xai": [
        "grok-1",
        "grok-2",
        "grok-2-latest"
    ],
    "mistral": [
        "mistral-large-latest",
        "pixtral-large-latest",
        "mistral-medium-latest",
        "mistral-moderation-latest",
        "ministral-3b-latest",
        "ministral-8b-latest",
        "open-mistral-nemo",
        "mistral-small-latest",
        "mistral-saba-latest",
        "codestral-latest",
        "mistral-ocr-latest"
    ],
    "deepseek": [
        "deepseek-chat",
        "deepseek-math",
        "deepseek-reasoning"
    ],
    "cohere": [
        "command",
        "command-light",
        "command-r",
        "command-r-plus"
    ],
    "gemini": [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ],
    "alibaba": [
        "qwen-turbo",
        "qwen-plus",
        "qwen-max"
    ],
    "openrouterai": [
        "openai/gpt-4-turbo",
        "anthropic/claude-3-opus",
        "mistralai/mistral-large",
        "meta-llama/llama-3-70b"
    ],
    "huggingface": [
        "meta-llama/Llama-2-7b-chat-hf",
        "meta-llama/Llama-3-8b-chat-hf",
        "mistralai/Mistral-7B-Instruct-v0.1",
        "google/gemma-7b-it"
    ]
}

def get_models_for_provider(provider_id):
    """
    Retrieve models for a specific provider.
    First, attempt to get models from the provider instance if registered,
    otherwise fall back to the static dictionary.
    
    :param provider_id: The ID of the provider
    :return: List of model names
    """
    provider = provider_registry.get_provider(provider_id)
    if provider:
        return provider.get_supported_models()
    return PROVIDER_MODELS.get(provider_id, [])

def get_all_models():
    """
    Retrieve all providers and their models.
    
    :return: Dictionary of providers and their models
    """
    result = {}
    for provider_id in provider_registry.get_available_provider_ids():
        result[provider_id] = get_models_for_provider(provider_id)
    return result
