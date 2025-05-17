import os
import importlib
import logging

class ProviderRegistry:
    """Registry for AI providers"""
    
    def __init__(self):
        self.providers = {}
        self.provider_classes = {}
        self.logger = logging.getLogger(__name__)
        
        # Dynamically discover and load providers
        self._load_providers()
        # Auto-register providers based on environment variables
        self._auto_register_providers()

    def _load_providers(self):
        """
        Dynamically discover and import provider classes from the ai_providers directory.
        Handles import errors gracefully to ensure robustness.
        """
        import glob
        import os.path

        provider_dir = os.path.dirname(os.path.abspath(__file__))
        provider_files = glob.glob(os.path.join(provider_dir, "*_provider.py"))
        
        for provider_file in provider_files:
            provider_id = os.path.basename(provider_file).replace('_provider.py', '')
            if provider_id in ['base']:  # Skip base provider or other non-specific files
                continue
                
            try:
                # Convert provider_id to PascalCase for class name
                provider_class_name = ''.join(word.capitalize() for word in provider_id.split('_')) + 'Provider'
                
                # Dynamically import the provider module
                module_name = f'app.services.ai_providers.{provider_id}_provider'
                module = importlib.import_module(module_name)
                
                # Get the provider class dynamically
                provider_class = getattr(module, provider_class_name)
                self.provider_classes[provider_id] = provider_class
                
                self.logger.info(f"Loaded provider: {provider_id}")
            except (ImportError, AttributeError) as e:
                self.logger.warning(f"Could not load provider {provider_id}: {str(e)}")
            except Exception as e:
                self.logger.error(f"Unexpected error loading provider {provider_id}: {str(e)}")

    def _auto_register_providers(self):
        """
        Automatically register providers based on API keys found in environment variables.
        The expected format for API keys in environment variables is PROVIDER_API_KEY.
        Skips providers that are not fully implemented or are abstract.
        """
        for provider_id in self.provider_classes.keys():
            env_var_name = f"{provider_id.upper()}_API_KEY"
            api_key = os.getenv(env_var_name)
            if api_key:
                try:
                    # Check if the provider class can be instantiated (not abstract)
                    provider_class = self.provider_classes[provider_id]
                    if hasattr(provider_class, '__abstractmethods__') and provider_class.__abstractmethods__:
                        self.logger.warning(f"Skipping auto-registration of abstract provider {provider_id}")
                        continue
                    self.register_provider(provider_id, api_key)
                    self.logger.info(f"Auto-registered provider {provider_id} using environment variable {env_var_name}")
                except ValueError as ve:
                    self.logger.warning(f"Failed to auto-register {provider_id}: {str(ve)}")
                except NotImplementedError as nie:
                    self.logger.warning(f"Skipping auto-registration of {provider_id} due to unimplemented features: {str(nie)}")
                except Exception as e:
                    self.logger.error(f"Unexpected error during auto-registration of {provider_id}: {str(e)}")

    def register_provider(self, provider_id, api_key):
        """
        Register a provider with the given API key.
        
        Args:
            provider_id (str): Lowercase provider identifier.
            api_key (str): API key for authentication.
            
        Returns:
            object: Registered provider instance.
            
        Raises:
            ValueError: If the provider is unknown or the API key is invalid.
            Exception: For other unexpected errors during registration.
        """
        if provider_id not in self.provider_classes:
            raise ValueError(f"Unknown provider: {provider_id}")
        
        provider_class = self.provider_classes[provider_id]
        
        try:
            provider = provider_class(api_key)
            if not provider.validate_api_key():
                raise ValueError(f"Invalid API key for {provider_id}")
            
            self.providers[provider_id] = provider
            self.logger.info(f"Successfully registered provider: {provider_id}")
            return provider
        except ValueError as ve:
            self.logger.error(f"Validation error for {provider_id}: {str(ve)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error registering {provider_id}: {str(e)}")
            raise

    def get_provider(self, provider_id):
        """
        Get the registered provider instance
        
        :param provider_id: Lowercase provider identifier
        :return: Provider instance or None
        """
        return self.providers.get(provider_id)

    def get_all_providers(self):
        """
        Get all registered providers
        
        :return: Dictionary of registered providers
        """
        return self.providers

    def get_available_provider_ids(self):
        """
        Get a list of all available provider IDs
        
        :return: List of provider identifiers
        """
        return list(self.provider_classes.keys())

    def get_default_provider(self):
        """
        Get the default provider (Groq)
        
        :return: Default provider instance
        """
        default_provider = os.getenv('DEFAULT_PROVIDER', 'groq')
        return self.get_provider(default_provider)

    def get_default_model(self):
        """
        Get the default model
        
        :return: Default model name
        """
        return os.getenv('DEFAULT_MODEL', 'llama-3.1-8b-instant')

# Create a global ProviderRegistry instance for the whole app
provider_registry = ProviderRegistry()
