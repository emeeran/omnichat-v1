from typing import Optional
import time

class ModelDiscoveryService:
    """Service to discover and cache available models from providers"""
    def __init__(self, provider_registry):
        self.provider_registry = provider_registry
        self.models_cache = {}
        self.last_updated = {}
        self.cache_ttl = 60 * 10  # 10 minutes

    def refresh_models(self, provider_id: Optional[str] = None):
        """Refresh models for specified provider or all providers"""
        if provider_id:
            provider = self.provider_registry.get_provider(provider_id)
            if provider:
                models = provider.get_available_models()
                self.models_cache[provider_id] = models
                self.last_updated[provider_id] = time.time()
        else:
            for pid in self.provider_registry.get_available_provider_ids():
                provider = self.provider_registry.get_provider(pid)
                if provider:
                    self._refresh_single_provider(pid, provider)

    def _refresh_single_provider(self, provider_id, provider):
        models = provider.get_available_models()
        self.models_cache[provider_id] = models
        self.last_updated[provider_id] = time.time()

    def get_available_models(self, provider_id: Optional[str] = None):
        """Get available models for specified provider or all providers"""
        now = time.time()
        if provider_id:
            if (provider_id not in self.models_cache or
                now - self.last_updated.get(provider_id, 0) > self.cache_ttl):
                self.refresh_models(provider_id)
            return self.models_cache.get(provider_id, [])
        else:
            # Refresh all if any cache is stale
            for pid in self.provider_registry.get_available_provider_ids():
                if (pid not in self.models_cache or
                    now - self.last_updated.get(pid, 0) > self.cache_ttl):
                    self.refresh_models()
                    break
            return self.models_cache
