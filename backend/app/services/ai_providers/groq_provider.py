from .base_provider import BaseProvider

import logging

class GroqProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "groq"
        self.logger = logging.getLogger(__name__)
        self._api_base_url = "https://api.groq.com/openai/v1"
        self.supported_models = {
            "production": [
                "llama-3.1-8b-instant",        # Fast with 128K context window
                "llama-3.1-70b-versatile",     # Meta's latest with 128K context window
                "llama-3.1-405b-reasoning",    # Large reasoning model with 128K context
                "llama3-8b-8192",              # Smaller, faster LLaMA 3 model
                "llama3-70b-8192",             # Standard LLaMA 3 model
                "gemma-7b-it",                 # Google's instruction-tuned model
                "gemma2-9b-it",                # Updated Google's instruction-tuned model
                "mixtral-8x7b-32768",          # Mixtral model
                "mistral-large-2407",          # Mistral's large model
            ],
            "speech": [
                "whisper-large-v3",            # Speech recognition model
                "whisper-large-v3-turbo",      # Faster speech recognition
                "distil-whisper-large-v3-en",  # Distilled English-specific model
            ],
            "preview": [
                "llama-3.2-1b-preview",        # LLaMA 3.2 preview model
                "llama-3.2-3b-preview",        # LLaMA 3.2 preview model
                "llama-3.2-11b-vision-preview",# LLaMA 3.2 vision model preview
                "llama-3.2-90b-vision-preview",# LLaMA 3.2 vision model preview
                "meta-llama/llama-4-maverick-17b-128e-instruct",  # LLaMA 4 preview
                "meta-llama/llama-4-scout-17b-16e-instruct",      # LLaMA 4 preview
                "meta-llama/Llama-Guard-4-12B",# Content safety model
                "llama-guard-3-8b",            # LLaMA Guard model for content safety
            ],
            "deprecated": [
                "llama2-70b-4096",             # Older LLaMA 2 model
                "llama2-7b-4096"               # Older smaller LLaMA 2 model
            ]
        }
        self._flat_supported_models = [
            model for category in self.supported_models.values() for model in category
        ]

    def get_supported_models(self):
        """
        Retrieve the list of supported models for this provider.
        Uses cached results if available, otherwise fetches from API.
        
        Returns:
            list: List of supported model names.
        """
        if hasattr(self, '_cached_models') and self._cached_models is not None:
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
                self.logger.info(f"Successfully fetched {len(self._cached_models)} models from Groq API")
                return self._cached_models
        except Exception as e:
            self.logger.error(f"Error fetching Groq models: {str(e)}")
        return self._flat_supported_models

    def get_api_endpoint(self):
        """
        Get the API endpoint for fetching models or other operations.
        
        Returns:
            str: API endpoint URL.
        """
        return f"{self._api_base_url}/models"

    def generate_completion(self, messages, model, options=None):
        """
        Generate a chat completion using the Groq API.
        
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
