from .base_provider import BaseProvider

class GoogleProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "google"
        self.supported_models = [
            "gemini-pro",
            "gemini-pro-vision",
            "palm-2"
        ]

    def get_api_endpoint(self):
        return "https://api.google.com/v1/models"
