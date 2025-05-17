from .base_provider import BaseProvider

class OpenrouteraiProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "openrouterai"
        self.supported_models = [
            "anthropic/claude-2",
            "anthropic/claude-instant-v1",
            "google/palm-2",
            "openai/gpt-3.5-turbo",
            "openai/gpt-4"
        ]

    def get_api_endpoint(self):
        return "https://api.openrouterai.com/v1/models"
