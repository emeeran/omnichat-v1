from .base_provider import BaseAIProvider
import openai

class OpenAIProvider(BaseAIProvider):
    """OpenAI API integration"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = openai.OpenAI(api_key=api_key)

    def get_available_models(self):
        try:
            models = self.client.models.list()
            # Filter for chat/completion models
            return [m.id for m in models.data if 'gpt' in m.id or 'chat' in m.id]
        except Exception as e:
            print(f"Error fetching OpenAI models: {e}")
            return []

    def generate_completion(self, messages, model, options=None):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **(options or {})
            )
            return {"text": response.choices[0].message.content}
        except Exception as e:
            print(f"Error generating OpenAI completion: {e}")
            return {"error": str(e)}

    def process_image(self, image_data, prompt, model, options=None):
        # Placeholder for OpenAI Vision API or similar
        return {"error": "Image processing not implemented for OpenAI"}

    def process_audio(self, audio_data, options=None):
        # Placeholder for OpenAI Whisper API or similar
        return {"error": "Audio processing not implemented for OpenAI"}
