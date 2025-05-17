import os
import json
import threading
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from app.services.ai_providers.provider_registry import ProviderRegistry

class ModelDiscoveryService:
    def __init__(self):
        self.provider_registry = ProviderRegistry()
        self.cache_file = os.path.join(os.path.dirname(__file__), 'model_cache.json')
        self.cache_expiry_hours = 24  # Cache models for 24 hours
        self.logger = logging.getLogger(__name__)
        self._start_periodic_model_refresh()

    def _start_periodic_model_refresh(self):
        """
        Start a background thread to periodically refresh models from all providers
        """
        def refresh_models():
            while True:
                try:
                    self._refresh_all_models()
                except Exception as e:
                    self.logger.error(f"Error in periodic model refresh: {e}")

                # Sleep for 24 hours between refreshes
                time.sleep(24 * 60 * 60)

        # Start the thread as a daemon so it doesn't block application shutdown
        thread = threading.Thread(target=refresh_models, daemon=True)
        thread.start()

    def _refresh_all_models(self):
        """
        Refresh models for all registered providers
        """
        provider_ids = self.provider_registry.get_available_provider_ids()

        for provider_id in provider_ids:
            try:
                # Attempt to fetch latest models
                models = self.fetch_latest_models(provider_id)

                # Log the refresh
                if models:
                    self.logger.info(f"Refreshed models for {provider_id}: {len(models)} models found")
                else:
                    self.logger.warning(f"No models found for {provider_id}")

            except Exception as e:
                self.logger.error(f"Failed to refresh models for {provider_id}: {e}")

    def get_supported_models(self, provider_id: str) -> List[str]:
        """
        Get supported models for a specific provider
        Attempts to fetch from provider, falls back to cached models
        """
        provider = self.provider_registry.get_provider(provider_id)
        if provider:
            return provider.get_supported_models()

        # Fallback to cached models if provider not registered
        return self._get_cached_models(provider_id)

    def _get_cached_models(self, provider_id: str) -> List[str]:
        """
        Retrieve cached models for a provider
        """
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)

            # Check if cache is valid and not expired
            if (provider_id in cache and
                'timestamp' in cache[provider_id] and
                'models' in cache[provider_id]):

                cached_time = datetime.fromisoformat(cache[provider_id]['timestamp'])
                if datetime.now() - cached_time < timedelta(hours=self.cache_expiry_hours):
                    return cache[provider_id]['models']
        except (FileNotFoundError, json.JSONDecodeError):
            # If cache file doesn't exist or is invalid, return empty list
            return []

        return []

    def update_model_cache(self, provider_id: str, models: List[str]):
        """
        Update the model cache for a specific provider
        """
        try:
            # Read existing cache or create new
            try:
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                cache = {}

            # Update cache for this provider
            cache[provider_id] = {
                'models': models,
                'timestamp': datetime.now().isoformat()
            }

            # Write updated cache
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error updating model cache for {provider_id}: {e}")

    def fetch_latest_models(self, provider_id: str) -> List[str]:
        """
        Fetch the latest supported models for a provider
        This method would ideally scrape or call the provider's API to get the most recent models
        For now, it uses the provider's predefined models
        """
        provider = self.provider_registry.get_provider(provider_id)
        if provider:
            models = provider.get_supported_models()
            self.update_model_cache(provider_id, models)
            return models
        return []

    def get_all_providers(self) -> List[Dict[str, str]]:
        """
        Get a list of all available providers
        """
        return [
            {"id": pid, "name": pid.capitalize()}
            for pid in self.provider_registry.get_available_provider_ids()
        ]
