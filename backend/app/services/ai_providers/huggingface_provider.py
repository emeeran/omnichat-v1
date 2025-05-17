from .base_provider import BaseProvider

class HuggingfaceProvider(BaseProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "huggingface"
        self.supported_models = [
            # Meta Llama 3 series
            "meta-llama/Llama-3.1-8B-Instruct",
            "meta-llama/Llama-3.1-70B-Instruct",
            "meta-llama/Llama-3-8B-Instruct",
            "meta-llama/Llama-3-70B-Instruct",
            # Mistral
            "mistralai/Mistral-7B-Instruct-v0.3",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            # Zephyr
            "HuggingFaceH4/zephyr-7b-beta",
            # Falcon
            "tiiuae/falcon-7b-instruct",
            # Google Flan
            "google/flan-t5-xxl",
            # BigScience
            "bigscience/bloom-560m",
            # OPT
            "facebook/opt-350m",
            # OpenAI GPT-2 (for compatibility)
            "openai-community/gpt2"
        ]

    def get_api_endpoint(self):
        return "https://api.huggingface.co/models"
