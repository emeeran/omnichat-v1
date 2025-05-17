import axios from 'axios';

const API_BASE_URL = '/api';

export const fetchProviders = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/providers`);
    return response.data;
  } catch (error) {
    console.error('Error fetching providers:', error);
    // Fallback providers if API call fails
    return [
      { id: 'deepseek', name: 'Deepseek' },
      { id: 'openai', name: 'OpenAI' },
      { id: 'anthropic', name: 'Anthropic' },
      { id: 'google', name: 'Google' },
      { id: 'mistral', name: 'Mistral' },
      { id: 'cohere', name: 'Cohere' },
      { id: 'groq', name: 'Groq' }
    ];
  }
};

export const fetchModels = async (providerId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/models/${providerId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching models for ${providerId}:`, error);
    
    // Fallback models for different providers
    const fallbackModels = {
      'deepseek': [
        { id: 'deepseek-chat', name: 'Deepseek Chat' },
        { id: 'deepseek-coder', name: 'Deepseek Coder' },
        { id: 'deepseek-llm', name: 'Deepseek LLM' }
      ],
      'openai': [
        { id: 'gpt-4.1-nano-2025-04-14', name: 'GPT-4.1 Nano (2025-04-14)' },
        { id: 'gpt-4.1-nano', name: 'GPT-4.1 Nano' },
        { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo' },
        { id: 'gpt-4', name: 'GPT-4' }
      ],
      'anthropic': [
        { id: 'claude-2.0', name: 'Claude 2.0' },
        { id: 'claude-instant-1.2', name: 'Claude Instant 1.2' }
      ],
      'google': [
        { id: 'gemini-pro', name: 'Gemini Pro' }
      ],
      'mistral': [
        { id: 'mistral-small', name: 'Mistral Small' },
        { id: 'mistral-medium', name: 'Mistral Medium' },
        { id: 'mistral-large', name: 'Mistral Large' }
      ],
      'cohere': [
        { id: 'command', name: 'Command' },
        { id: 'command-light', name: 'Command Light' },
        { id: 'command-r', name: 'Command R' }
      ],
      'groq': [
        { id: 'llama2-70b-4096', name: 'Llama2 70B' },
        { id: 'mixtral-8x7b-32768', name: 'Mixtral 8x7B' }
      ]
    };
    
    return fallbackModels[providerId.toLowerCase()] || [];
  }
};

export const registerProvider = async (providerId, apiKey) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/providers/register`, {
      provider_id: providerId,
      api_key: apiKey
    });
    return response.data;
  } catch (error) {
    console.error(`Error registering provider ${providerId}:`, error);
    throw error;
  }
};

export const sendMessage = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat/completions`, data);
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    return { error: error.message };
  }
};

export const streamMessage = async (data, onChunk) => {
  try {
    const response = await fetch(`/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let result = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      result += chunk;
      onChunk(chunk);
    }

    return { content: result };
  } catch (error) {
    console.error('Error streaming message:', error);
    return { error: error.message };
  }
};
