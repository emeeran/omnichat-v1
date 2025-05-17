from .base_provider import BaseProvider

class MistralProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "mistral"
        self.supported_models = [
            # Premier models
            "codestral-latest",
            "mistral-large-latest",
            "pixtral-large-latest",
            "mistral-medium-latest",
            "mistral-saba-latest",
            "ministral-3b-latest",
            "ministral-8b-latest",
            "mistral-embed",
            "mistral-moderation-latest",
            "mistral-ocr-latest",
            # Free models
            "mistral-small-latest",
            "pixtral-12b-2409",
            # Research models
            "open-mistral-nemo",
            "open-codestral-mamba",
            "open-mixtral-8x7b",
            "open-mixtral-8x22b",
            # Legacy models (for compatibility)
            "mistral-small-2402",
            "mistral-large-2402",
            "mistral-large-2407"
        ]

    def get_api_endpoint(self):
        return "https://api.mistral.com/v1/models"
