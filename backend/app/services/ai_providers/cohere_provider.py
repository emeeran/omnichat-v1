from .base_provider import BaseProvider

class CohereProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "cohere"
        self.supported_models = [
            # Command A Series
            "command-a-03-2025",
            
            # Command R Series
            "command-r7b-12-2024",
            "command-r-plus-04-2024",
            "command-r-plus", # alias for command-r-plus-04-2024
            "command-r-08-2024",
            "command-r-03-2024",
            "command-r", # alias for command-r-03-2024
            
            # Legacy Command Series
            "command",
            "command-nightly",
            "command-light",
            "command-light-nightly",
            
            # Aya Series
            "c4ai-aya-expanse-8b",
            "c4ai-aya-expanse-32b",
            "c4ai-aya-vision-8b",
            "c4ai-aya-vision-32b"
        ]

    def get_supported_models(self):
        return self.supported_models
