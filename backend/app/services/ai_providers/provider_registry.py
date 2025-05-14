import os
from app.services.ai_providers.openai_provider import OpenAIProvider
from app.services.ai_providers.anthropic_provider import AnthropicProvider
from app.services.ai_providers.google_provider import GoogleAIProvider
# Import other providers as needed

class ProviderRegistry:
    """Registry for AI providers"""
    
    def __init__(self):
        self.providers = {}
        self.provider_classes = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "google": GoogleAIProvider,
            # Add other providers as needed
        }
        # Auto-register providers with API keys from environment
        self._auto_register_from_env()

    def _auto_register_from_env(self):
        env_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "google": os.getenv("GOOGLE_AI_API_KEY"),
            # Add other providers as needed
        }
        for pid, key in env_keys.items():
            if key:
                try:
                    self.register_provider(pid, key)
                except Exception as e:
                    print(f"Failed to auto-register {pid}: {e}")

    def register_provider(self, provider_id, api_key):
        """Register a provider with the given API key"""
        if provider_id not in self.provider_classes:
            raise ValueError(f"Unknown provider: {provider_id}")
            
        provider_class = self.provider_classes[provider_id]
        self.providers[provider_id] = provider_class(api_key)
        return self.providers[provider_id]
        
    def get_provider(self, provider_id):
        """Get the provider with the given ID"""
        return self.providers.get(provider_id)
        
    def get_all_providers(self):
        """Get all registered providers"""
        return self.providers
        
    def get_available_provider_ids(self):
        """Get a list of all available provider IDs"""
        return list(self.provider_classes.keys())
