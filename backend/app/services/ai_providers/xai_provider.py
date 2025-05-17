from .base_provider import BaseProvider

class XaiProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "xai"
        self.supported_models = [
            # Latest Grok models
            "grok-3",  # Updated to full release if available by May 2025
            "grok-3-preview",
            
            # Grok 2 series - Vision capable models
            "grok-2",
            "grok-2-vision",
            "grok-2-latest",
            "grok-2-vision-latest",
            
            # Older models
            "grok-1.5",
            "grok-1"
        ]

    def get_api_endpoint(self):
        return "https://api.xai.com/v1/models"
