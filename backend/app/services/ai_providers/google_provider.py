from .base_provider import BaseAIProvider
import os
try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GoogleAIProvider(BaseAIProvider):
    """Google AI API integration"""
    def __init__(self, api_key=None):
        super().__init__(api_key or os.getenv("GOOGLE_AI_API_KEY", ""))
        if genai:
            genai.configure(api_key=self.api_key)
        self.client = genai

    def _determine_capabilities(self, model_name):
        caps = ["text"]
        if "vision" in model_name.lower() or "gemini-pro-vision" in model_name.lower():
            caps.append("vision")
        return caps

    def get_available_models(self):
        if not self.client:
            print("[GoogleAIProvider] Google Generative AI SDK not installed.")
            return []
        try:
            models = self.client.list_models()
            result = []
            for m in models:
                if "gemini" in m.name or "chat" in m.name:
                    result.append({
                        "id": m.name,
                        "name": getattr(m, "display_name", m.name),
                        "capabilities": self._determine_capabilities(m.name),
                        "provider": "google"
                    })
            return result
        except Exception as e:
            print(f"[GoogleAIProvider] Error fetching Google models: {e}")
            return []

    def generate_completion(self, messages, model, options=None):
        if not self.client:
            print("[GoogleAIProvider] Google Generative AI SDK not installed.")
            return {"error": "Google Generative AI SDK not installed"}
        try:
            prompt = "\n".join([m["content"] for m in messages if m["role"] == "user"])
            model_obj = self.client.GenerativeModel(model)
            response = model_obj.generate_content(prompt)
            text = getattr(response, "text", None)
            usage = getattr(response, "usage_metadata", None)
            result = {"text": text or ""}
            if usage:
                result["usage"] = {
                    "prompt_tokens": getattr(usage, "prompt_token_count", None),
                    "completion_tokens": getattr(usage, "candidates_token_count", None),
                    "total_tokens": getattr(usage, "total_token_count", None)
                }
            print(f"[GoogleAIProvider] Completion success for model {model}")
            return result
        except Exception as e:
            print(f"[GoogleAIProvider] Error generating Google completion (model={model}): {e}")
            return {"error": str(e)}

    def process_image(self, image_data, prompt, model, options=None):
        print("[GoogleAIProvider] Image processing not implemented.")
        return {"error": "Image processing not implemented for Google AI"}

    def process_audio(self, audio_data, options=None):
        print("[GoogleAIProvider] Audio processing not implemented.")
        return {"error": "Audio processing not implemented for Google AI"}
