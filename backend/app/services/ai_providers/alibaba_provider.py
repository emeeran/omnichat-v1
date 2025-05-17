from .base_provider import BaseProvider
import logging

class AlibabaProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "alibaba"
        self.logger = logging.getLogger(__name__)
        self._api_base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        self._cached_models = None
        self.supported_models = [
            # QwQ Reasoning Model
            "qwq-plus",
            
            # Commercial Qwen Models
            "qwen-max",
            "qwen-max-latest",
            "qwen-max-2025-01-25",
            
            "qwen-plus",
            "qwen-plus-latest",
            "qwen-plus-2025-04-28",
            "qwen-plus-2025-01-25",
            
            "qwen-turbo",
            "qwen-turbo-latest",
            "qwen-turbo-2025-04-28",
            "qwen-turbo-2024-11-01",
            
            # Visual Reasoning Model
            "qvq-max",
            "qvq-max-latest",
            "qvq-max-2025-03-25",
            
            # Visual Models
            "qwen-vl-max",
            "qwen-vl-max-latest",
            "qwen-vl-max-2025-04-08",
            
            "qwen-vl-plus",
            "qwen-vl-plus-latest",
            "qwen-vl-plus-2025-01-25",
            
            # Open Source Models
            "qwen3-235b-a22b",
            "qwen3-32b",
            "qwen3-30b-a3b",
            "qwen3-14b",
            "qwen3-8b",
            "qwen3-4b",
            "qwen3-1.7b",
            "qwen3-0.6b",
            
            # Qwen 2.5 Models
            "qwen2.5-72b-instruct",
            "qwen2.5-32b-instruct",
            "qwen2.5-14b-instruct",
            "qwen2.5-7b-instruct",
            "qwen2.5-14b-instruct-1m",
            "qwen2.5-7b-instruct-1m",
            
            # Omni-modal
            "qwen2.5-omni-7b"
        ]

    def get_supported_models(self):
        """
        Retrieve the list of supported models for this provider.
        Uses cached results if available, otherwise fetches from API.
        
        Returns:
            list: List of supported model names.
        """
        if self._cached_models is not None:
            return self._cached_models
            
        import requests
        headers = {
            "Authorization": f"Bearer {self._api_key}"
        }
        try:
            response = requests.get(self.get_api_endpoint(), headers=headers, timeout=10)
            if response.status_code == 200:
                models_data = response.json().get('data', [])
                self._cached_models = [model['id'] for model in models_data]
                self.logger.info(f"Successfully fetched {len(self._cached_models)} models from Alibaba API")
                return self._cached_models
        except Exception as e:
            self.logger.error(f"Error fetching Alibaba models: {str(e)}")
        return self.supported_models

    def get_api_endpoint(self):
        """
        Get the API endpoint for fetching models.
        
        Returns:
            str: API endpoint URL.
        """
        return f"{self._api_base_url}/models"

    def generate_completion(self, messages, model, options=None):
        """
        Generate a chat completion using the Alibaba Cloud DashScope API.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys.
            model (str): String specifying the model to use.
            options (dict, optional): Dictionary of optional parameters like temperature, max_tokens.
            
        Returns:
            dict: Dictionary with the completion result.
            
        Raises:
            Exception: If the API request fails.
        """
        import requests
        options = options or {}
        endpoint = f"{self._api_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": options.get("temperature", 0.7),
            "max_tokens": options.get("max_tokens", 1000),
            "stream": options.get("stream", False)
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "finish_reason": result["choices"][0]["finish_reason"],
                    "usage": {
                        "prompt_tokens": result["usage"]["prompt_tokens"],
                        "completion_tokens": result["usage"]["completion_tokens"],
                        "total_tokens": result["usage"]["total_tokens"]
                    }
                }
            else:
                error_msg = f"Error generating completion: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            self.logger.error(f"Unexpected error in generate_completion: {str(e)}")
            raise
