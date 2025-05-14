class BaseAIProvider:
    """Base class for all AI providers"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    async def get_available_models(self):
        """Fetch available models from the provider"""
        raise NotImplementedError
        
    async def generate_completion(self, messages, model, options=None):
        """Generate a completion for the given messages"""
        raise NotImplementedError
        
    async def process_image(self, image_data, prompt, model, options=None):
        """Process an image with the given prompt"""
        raise NotImplementedError
        
    async def process_audio(self, audio_data, options=None):
        """Process audio data (transcription/analysis)"""
        raise NotImplementedError
    
    async def generate_image(self, prompt, options=None):
        """Generate an image based on the prompt"""
        raise NotImplementedError
