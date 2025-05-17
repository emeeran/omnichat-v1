from dotenv import load_dotenv
import os
# Explicitly load .env from project root
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env')), override=True)
from app.services.ai_providers.provider_registry import ProviderRegistry

provider_registry = ProviderRegistry()

# Auto-register providers with API keys from .env at import time
for provider, env_var in [
    ("openai", "OPENAI_API_KEY"),
    ("anthropic", "ANTHROPIC_API_KEY"),
    ("google", "GOOGLE_AI_API_KEY"),
    ("deepseek", "DEEPSEEK_API_KEY"),
    ("groq", "GROQ_API_KEY"),
    ("mistral", "MISTRAL_API_KEY"),
    ("cohere", "COHERE_API_KEY"),
    ("gemini", "GEMINI_API_KEY"),
    ("alibaba", "ALIBABA_API_KEY"),
    ("openrouterai", "OPENROUTERAI_API_KEY"),
    ("huggingface", "HUGGINGFACE_API_KEY"),
    ("xai", "XAI_API_KEY")
]:
    api_key = os.getenv(env_var)
    print(f"[DEBUG] {provider}: {env_var}={api_key}")
    if api_key:
        try:
            provider_registry.register_provider(provider, api_key)
            print(f"[DEBUG] Registered provider: {provider}")
        except Exception as e:
            print(f"[DEBUG] Failed to register provider {provider}: {e}")
