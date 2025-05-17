from .base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "gemini"
        self.supported_models = [
            # Gemini 2.5
            "gemini-2.5-flash-preview-04-17",
            "gemini-2.5-pro-preview-05-06",
            # Gemini 2.0
            "gemini-2.0-flash",
            "gemini-2.0-flash-preview-image-generation",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash-live-001",
            # Gemini 1.5
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro",
            # Embeddings and experimental
            "gemini-embedding-exp",
            # Imagen and Veo (image/video generation)
            "imagen-3.0-generate-002",
            "veo-2.0-generate-001"
        ]

    def get_api_endpoint(self):
        return "https://api.gemini.com/v1/models"
