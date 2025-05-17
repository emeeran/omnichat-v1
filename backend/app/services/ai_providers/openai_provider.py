from .base_provider import BaseProvider

import logging

class OpenaiProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "openai"
        self.logger = logging.getLogger(__name__)
        self._api_base_url = "https://api.openai.com/v1"
        self._cached_models = None
        self.supported_models = [
            # GPT-4o (Omni)
            "gpt-4o-2024-05-13",
            "gpt-4o",
            # GPT-4 Turbo
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo",
            # GPT-4
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4",
            # GPT-3.5 Turbo
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo",
            # GPT-4.1 Nano (experimental, if available)
            "gpt-4.1-nano-2025-04-14",
            "gpt-4.1-nano"
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
                self._cached_models = [model['id'] for model in models_data if 'gpt' in model['id'].lower()]
                self.logger.info(f"Successfully fetched {len(self._cached_models)} models from OpenAI API")
                return self._cached_models
        except Exception as e:
            self.logger.error(f"Error fetching OpenAI models: {str(e)}")
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
        Generate a chat completion using the OpenAI API.
        
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
            elif (response.status_code in [403, 404, 400]) and any(error in response.text.lower() for error in ["model_not_found", "not supported", "audio"]):
                error_msg = f"Model {model} not compatible: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                # Fallback to a list of known compatible chat models
                fallback_models = ["gpt-4o-mini", "gpt-4o", "gpt-4"]
                supported_models = self.get_supported_models()
                for fallback_model in fallback_models:
                    if model != fallback_model and fallback_model in supported_models:
                        self.logger.info(f"Falling back to {fallback_model} due to compatibility issue with {model}")
                        payload["model"] = fallback_model
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
                            self.logger.error(f"Error with fallback model {fallback_model}: {response.status_code} - {response.text}")
                raise Exception(error_msg)
            else:
                error_msg = f"Error generating completion: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            self.logger.error(f"Unexpected error in generate_completion: {str(e)}")
            raise
