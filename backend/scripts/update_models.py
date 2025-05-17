#!/usr/bin/env python3
"""
Script to update the list of supported models for all AI providers.
Intended to be run weekly to fetch the latest models from provider APIs.
"""

import os
import sys
import logging
from app.services.ai_providers.provider_registry import provider_registry

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_all_models():
    """
    Update the model lists for all registered providers.
    Forces a refresh by clearing any cached model lists.
    """
    logger.info("Starting model update for all providers...")
    providers = provider_registry.get_all_providers()
    
    if not providers:
        logger.warning("No providers are currently registered. Ensure API keys are set in environment variables.")
        return
    
    for provider_id, provider in providers.items():
        try:
            # Clear any cached models to force a refresh
            if hasattr(provider, '_cached_models'):
                provider._cached_models = None
                logger.info(f"Cleared cached models for {provider_id}")
            
            # Fetch the latest models
            models = provider.get_supported_models()
            logger.info(f"Updated models for {provider_id}: fetched {len(models)} models")
        except Exception as e:
            logger.error(f"Error updating models for {provider_id}: {str(e)}")
    
    logger.info("Model update completed for all providers.")

if __name__ == "__main__":
    # Ensure the script can find the app module
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    update_all_models()
