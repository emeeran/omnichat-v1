from abc import ABC, abstractmethod
import requests

class BaseProvider(ABC):
    """
    Abstract base class for AI providers
    Defines the interface for all provider implementations
    """
    def __init__(self, api_key):
        """
        Initialize the provider with an API key
        
        :param api_key: API key for authentication
        """
        self._api_key = api_key
        self.name = None  # To be set by child classes
        self.supported_models = []  # To be set by child classes

    @abstractmethod
    def get_supported_models(self):
        """
        Retrieve the list of supported models for this provider
        
        :return: List of supported model names
        """
        pass

    def validate_api_key(self):
        """
        Validate the API key for the provider
        
        :return: Boolean indicating if the API key is valid
        """
        # Basic validation, can be overridden by specific providers
        if not self._api_key or not isinstance(self._api_key, str):
            return False

        # Check if the API key is valid by making a test request
        try:
            response = requests.get(
                self.get_api_endpoint(),
                headers={'Authorization': f'Bearer {self._api_key}'}
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_api_endpoint(self):
        """
        Get the API endpoint for the provider
        
        :return: API endpoint URL
        """
        # This method should be overridden by specific providers
        raise NotImplementedError("API endpoint not implemented")

    def __str__(self):
        """
        String representation of the provider
        
        :return: Provider name
        """
        return self.name or 'Unnamed Provider'
