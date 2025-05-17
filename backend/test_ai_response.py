import requests
import json
import os
import sys

# Assuming the backend server is running on localhost:5001
BASE_URL = "http://localhost:5000/api/chat"

def test_ai_response():
    """
    Test the AI response system with a sample query.
    """
    # Use the default provider and model from environment or hardcoded values
    provider = os.getenv('DEFAULT_PROVIDER', 'deepseek')
    model = os.getenv('DEFAULT_MODEL', 'deepseek-chat')
    
    # Sample query
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Hello, can you tell me about the weather today?"}
    ]
    
    # Prepare the request payload
    payload = {
        "provider": provider,
        "model": model,
        "messages": messages,
        "options": {}
    }
    
    try:
        # Send POST request to the chat completions endpoint
        response = requests.post(f"{BASE_URL}/completions", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("AI Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Ensure the backend server is running on localhost:5000.")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_all_providers():
    """
    Test the AI response system for all providers and their latest models.
    """
    providers_and_models = [
        ("cohere", [
            "command-a-03-2025", "command-r7b-12-2024", "command-r-plus-04-2024", "command-r-plus", "command-r-08-2024", "command-r-03-2024", "command-r", "command", "command-nightly", "command-light", "command-light-nightly", "c4ai-aya-expanse-8b", "c4ai-aya-expanse-32b", "c4ai-aya-vision-8b", "c4ai-aya-vision-32b"
        ]),
        ("xai", [
            "grok-3", "grok-3-preview", "grok-2", "grok-2-vision", "grok-2-latest", "grok-2-vision-latest", "grok-1.5", "grok-1"
        ]),
        ("deepseek", [
            "deepseek-chat", "deepseek-reasoner", "deepseek-coder", "deepseek-llm", "deepseek-chat-v2", "deepseek-coder-v2", "deepseek-math-7b"
        ]),
        ("alibaba", [
            "qwq-plus", "qwen-max", "qwen-max-latest", "qwen-max-2025-01-25", "qwen-plus", "qwen-plus-latest", "qwen-plus-2025-04-28", "qwen-plus-2025-01-25", "qwen-turbo", "qwen-turbo-latest", "qwen-turbo-2025-04-28", "qwen-turbo-2024-11-01", "qvq-max", "qvq-max-latest", "qvq-max-2025-03-25", "qwen-vl-max", "qwen-vl-max-latest", "qwen-vl-max-2025-04-08", "qwen-vl-plus", "qwen-vl-plus-latest", "qwen-vl-plus-2025-01-25", "qwen3-235b-a22b", "qwen3-32b", "qwen3-30b-a3b", "qwen3-14b", "qwen3-8b", "qwen3-4b", "qwen3-1.7b", "qwen3-0.6b"
        ]),
        ("groq", [
            "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "llama3-8b-8192", "gemma2-9b-it", "whisper-large-v3", "whisper-large-v3-turbo", "distil-whisper-large-v3-en", "meta-llama/llama-4-maverick-17b-128e-instruct", "meta-llama/llama-4-scout-17b-16e-instruct", "meta-llama/Llama-Guard-4-12B", "mistral-saba-24b", "qwen-qwq-32b", "deepseek-r1-distill-llama-70b", "mixtral-8x7b-32768", "llama2-70b-4096"
        ]),
        ("anthropic", [
            "claude-3-7-sonnet-20250219", "claude-3-7-sonnet-latest", "claude-3-5-sonnet-20241022", "claude-3-5-sonnet-latest", "claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-3-5-haiku-latest", "claude-3-opus-20240229", "claude-3-opus-latest", "claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-2.0", "claude-instant-1.2"
        ]),
        ("gemini", [
            "gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-preview-05-06", "gemini-2.0-flash", "gemini-2.0-flash-preview-image-generation", "gemini-2.0-flash-lite", "gemini-2.0-flash-live-001", "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro", "gemini-embedding-exp", "imagen-3.0-generate-002", "veo-2.0-generate-001"
        ]),
        ("mistral", [
            "codestral-latest", "mistral-large-latest", "pixtral-large-latest", "mistral-medium-latest", "mistral-saba-latest", "ministral-3b-latest", "ministral-8b-latest", "mistral-embed", "mistral-moderation-latest", "mistral-ocr-latest", "mistral-small-latest", "pixtral-12b-2409", "open-mistral-nemo", "open-codestral-mamba", "open-mixtral-8x7b", "open-mixtral-8x22b", "mistral-small-2402", "mistral-large-2402", "mistral-large-2407"
        ]),
        ("openai", [
            "gpt-4o-2024-05-13", "gpt-4o", "gpt-4-turbo-2024-04-09", "gpt-4-turbo", "gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-4", "gpt-3.5-turbo-0125", "gpt-3.5-turbo-1106", "gpt-3.5-turbo", "gpt-4.1-nano-2025-04-14", "gpt-4.1-nano"
        ]),
        ("huggingface", [
            "meta-llama/Llama-3.1-8B-Instruct", "meta-llama/Llama-3.1-70B-Instruct", "meta-llama/Llama-3-8B-Instruct", "meta-llama/Llama-3-70B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3", "mistralai/Mixtral-8x7B-Instruct-v0.1", "HuggingFaceH4/zephyr-7b-beta", "tiiuae/falcon-7b-instruct", "google/flan-t5-xxl", "bigscience/bloom-560m", "facebook/opt-350m", "openai-community/gpt2"
        ]),
    ]

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Respond in markdown with at least one heading, a list, and a code block."},
        {"role": "user", "content": "Show me a markdown example with a heading, a list, and a code block."}
    ]

    for provider, models in providers_and_models:
        for model in models[:1]:  # Only test the first/latest model for each provider for speed
            payload = {
                "provider": provider,
                "model": model,
                "messages": messages,
                "options": {}
            }
            print(f"\nTesting provider: {provider}, model: {model}")
            try:
                response = requests.post(f"{BASE_URL}/completions", json=payload, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    print("AI Response:")
                    print(json.dumps(data, indent=2))
                    if 'content' in data and ("#" in data['content'] or "```" in data['content']):
                        print("Markdown detected in response.")
                    else:
                        print("Warning: Markdown not detected in response content.")
                else:
                    print(f"Error: Received status code {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"Error with provider {provider}, model {model}: {str(e)}")

if __name__ == "__main__":
    print("Testing AI response system...")
    test_ai_response()
    print("\nTesting all providers and latest models...")
    test_all_providers()
