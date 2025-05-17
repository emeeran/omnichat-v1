from .base_provider import BaseProvider

class DeepseekProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "deepseek"
        self.supported_models = [
            # Current main models
            "deepseek-chat",    # DeepSeek-V3
            "deepseek-reasoner", # DeepSeek-R1
            
            # Legacy models
            "deepseek-coder",
            "deepseek-llm",
            "deepseek-chat-v2",
            "deepseek-coder-v2",
            "deepseek-math-7b"
        ]

    def get_supported_models(self):
        return self.supported_models
