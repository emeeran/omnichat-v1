from .base_provider import BaseAIProvider
import os
try:
    import anthropic
except ImportError:
    anthropic = None

class AnthropicProvider(BaseAIProvider):
    """Anthropic API integration"""
    CLAUDE_3_MODELS = [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        # Add future Claude 3.x models here
    ]

    def __init__(self, api_key=None):
        super().__init__(api_key or os.getenv("ANTHROPIC_API_KEY", ""))
        if anthropic:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def get_available_models(self):
        if not self.client:
            return []
        try:
            return self.CLAUDE_3_MODELS + [
                "claude-2.1",
                "claude-2.0",
                "claude-instant-1.2"
            ]
        except Exception as e:
            print(f"Error fetching Anthropic models: {e}")
            return []

    def generate_completion(self, messages, model, options=None):
        if not self.client:
            return {"error": "Anthropic SDK not installed"}
        try:
            if model in self.CLAUDE_3_MODELS:
                # Use Messages API for Claude 3
                system = None
                msg_list = []
                for m in messages:
                    if m["role"] == "system":
                        system = m["content"]
                    elif m["role"] == "user":
                        msg_list.append({"role": "user", "content": m["content"]})
                    elif m["role"] == "assistant":
                        msg_list.append({"role": "assistant", "content": m["content"]})
                kwargs = {
                    "model": model,
                    "max_tokens": options.get("max_tokens", 1024) if options else 1024,
                    "messages": msg_list
                }
                if system and isinstance(system, str) and system.strip():
                    kwargs["system"] = system
                response = self.client.messages.create(**kwargs)
                return {"text": response.content[0].text if response.content else ""}
            else:
                # Use completions API for Claude 2 and below
                prompt = ""
                for m in messages:
                    if m["role"] == "user":
                        prompt += "\n\nHuman: " + m["content"]
                    elif m["role"] == "assistant":
                        prompt += "\n\nAssistant: " + m["content"]
                if not prompt.strip().startswith("Human:"):
                    prompt = "\n\nHuman:" + prompt
                if not prompt.rstrip().endswith("Assistant:"):
                    prompt += "\n\nAssistant:"
                response = self.client.completions.create(
                    model=model,
                    prompt=prompt,
                    max_tokens_to_sample=options.get("max_tokens", 1024) if options else 1024
                )
                return {"text": response.completion}
        except Exception as e:
            print(f"Error generating Anthropic completion: {e}")
            return {"error": str(e)}

    def process_image(self, image_data, prompt, model, options=None):
        return {"error": "Image processing not implemented for Anthropic"}

    def process_audio(self, audio_data, options=None):
        return {"error": "Audio processing not implemented for Anthropic"}
