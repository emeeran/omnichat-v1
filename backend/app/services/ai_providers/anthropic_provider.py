from .base_provider import BaseProvider

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "anthropic"
        self.supported_models = [
            # Claude 3.7 Sonnet (latest, extended thinking, 200K context)
            "claude-3-7-sonnet-20250219",
            "claude-3-7-sonnet-latest",
            # Claude 3.5 Sonnet (latest, 200K context)
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-latest",
            "claude-3-5-sonnet-20240620",
            # Claude 3.5 Haiku (latest, 200K context)
            "claude-3-5-haiku-20241022",
            "claude-3-5-haiku-latest",
            # Claude 3 Opus (200K context)
            "claude-3-opus-20240229",
            "claude-3-opus-latest",
            # Claude 3 Sonnet (legacy, 200K context)
            "claude-3-sonnet-20240229",
            # Claude 3 Haiku (legacy, 200K context)
            "claude-3-haiku-20240307",
            # Legacy Claude 2.x and instant
            "claude-2.0",
            "claude-instant-1.2"
        ]

    def get_api_endpoint(self):
        return "https://api.anthropic.com/v1/models"
