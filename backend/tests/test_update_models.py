#!/usr/bin/env python3
"""
Unit tests for the model update functionality.
"""

import unittest
import os
import sys
import logging
from unittest.mock import patch, MagicMock

# Ensure the script can find the app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.ai_providers.provider_registry import provider_registry
from scripts.update_models import update_all_models

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestUpdateModels(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.provider_registry = provider_registry
        self.providers = {
            'openai': MagicMock(),
            'groq': MagicMock()
        }
        for provider in self.providers.values():
            provider.get_supported_models.return_value = ['model1', 'model2']
            provider._cached_models = None

    @patch('app.services.ai_providers.provider_registry.provider_registry.get_all_providers')
    def test_update_all_models_success(self, mock_get_all_providers):
        """Test successful update of models for all providers."""
        mock_get_all_providers.return_value = self.providers
        
        with patch('logging.Logger.info') as mock_info, patch('logging.Logger.error') as mock_error:
            update_all_models()
            
            for provider_id, provider in self.providers.items():
                self.assertIsNone(provider._cached_models, f"Cached models should be cleared for {provider_id}")
                provider.get_supported_models.assert_called_once()
            mock_info.assert_called()
            mock_error.assert_not_called()

    @patch('app.services.ai_providers.provider_registry.provider_registry.get_all_providers')
    def test_update_all_models_empty_providers(self, mock_get_all_providers):
        """Test update models when no providers are registered."""
        mock_get_all_providers.return_value = {}
        
        with patch('logging.Logger.warning') as mock_warning:
            update_all_models()
            mock_warning.assert_called_with("No providers are currently registered. Ensure API keys are set in environment variables.")

    @patch('app.services.ai_providers.provider_registry.provider_registry.get_all_providers')
    def test_update_all_models_error(self, mock_get_all_providers):
        """Test update models when fetching models raises an exception."""
        error_provider = MagicMock()
        error_provider.get_supported_models.side_effect = Exception("API error")
        error_provider._cached_models = None
        mock_get_all_providers.return_value = {'error_provider': error_provider}
        
        with patch('logging.Logger.error') as mock_error:
            update_all_models()
            mock_error.assert_called_with("Error updating models for error_provider: API error")

if __name__ == '__main__':
    unittest.main()
