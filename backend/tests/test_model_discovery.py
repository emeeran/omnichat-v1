import unittest
import os
import sys
import tempfile
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.model_discovery import ModelDiscoveryService

class TestModelDiscoveryService(unittest.TestCase):
    def setUp(self):
        self.service = ModelDiscoveryService()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_file = os.path.join(self.temp_dir.name, 'test_model_cache.json')
        self.service.cache_file = self.cache_file

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_supported_models(self):
        # Test with no cached models
        models = self.service.get_supported_models('test_provider')
        self.assertEqual(models, [])

        # Test with cached models
        cache_data = {
            'test_provider': {
                'models': ['model1', 'model2'],
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat()
            }
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)

        models = self.service.get_supported_models('test_provider')
        self.assertEqual(models, ['model1', 'model2'])

    def test_update_model_cache(self):
        self.service.update_model_cache('test_provider', ['model1', 'model2'])

        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)

        self.assertIn('test_provider', cache_data)
        self.assertEqual(cache_data['test_provider']['models'], ['model1', 'model2'])
        self.assertIn('timestamp', cache_data['test_provider'])

    @patch('app.services.model_discovery.ProviderRegistry')
    def test_fetch_latest_models(self, MockProviderRegistry):
        mock_provider = MagicMock()
        mock_provider.get_supported_models.return_value = ['model3', 'model4']
        MockProviderRegistry.return_value.get_provider.return_value = mock_provider

        # Ensure the provider registry returns the mock provider for 'test_provider'
        self.service.provider_registry = MockProviderRegistry.return_value

        models = self.service.fetch_latest_models('test_provider')
        self.assertEqual(models, ['model3', 'model4'])

        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)

        self.assertIn('test_provider', cache_data)
        self.assertEqual(cache_data['test_provider']['models'], ['model3', 'model4'])

    def test_get_all_providers(self):
        providers = self.service.get_all_providers()
        self.assertIsInstance(providers, list)
        self.assertGreater(len(providers), 0)
        for provider in providers:
            self.assertIn('id', provider)
            self.assertIn('name', provider)

if __name__ == '__main__':
    unittest.main()
