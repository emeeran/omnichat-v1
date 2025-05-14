// src/services/api.js

const API_BASE = 'http://localhost:5001/api';

export async function fetchProviders() {
  try {
    const res = await fetch(`${API_BASE}/providers`);
    if (!res.ok) throw new Error('Failed to fetch providers');
    const response = await res.json();
    return response.providers || [];
  } catch (error) {
    console.error('Error fetching providers:', error);
    return [];
  }
}

export async function fetchModels(providerId) {
  try {
    const res = await fetch(`${API_BASE}/providers/${providerId}/models`);
    if (!res.ok) throw new Error('Failed to fetch models');
    const response = await res.json();
    return response.models || [];
  } catch (error) {
    console.error('Error fetching models:', error);
    return [];
  }
}

export async function sendMessage({ provider, model, messages, options }) {
  // Modify the last user message to request Markdown formatting
  const modifiedMessages = messages.map((msg, index) => {
    if (index === messages.length - 1 && msg.role === 'user') {
      return {
        ...msg,
        content: msg.content + "\n\nPlease format your response using Markdown syntax (e.g., **bold**, *italic*, # Heading, - lists, ```code blocks```, etc.) for better readability."
      };
    }
    return msg;
  });
  try {
    const res = await fetch(`${API_BASE}/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider, model, messages: modifiedMessages, options })
    });
    const text = await res.text();
    console.log('Raw response from backend (full text):', text);
    try {
      const response = JSON.parse(text);
      console.log('Parsed response structure (detailed):', JSON.stringify(response, null, 2));
      // Extract content from various possible response structures
      let content = '';
      if (response.text) {
        content = response.text;
        console.log('Extracted content from "text" field:', content);
      } else if (response.content) {
        content = response.content;
        console.log('Extracted content from "content" field:', content);
      } else if (response.data && response.data.content) {
        content = response.data.content;
        console.log('Extracted content from "data.content" field:', content);
      } else if (response.choices && response.choices.length > 0 && response.choices[0].message) {
        content = response.choices[0].message.content || 'No content in response';
        console.log('Extracted content from "choices[0].message.content" field:', content);
      } else {
        content = 'Unable to extract response content';
        console.log('Unexpected response structure, no content found:', JSON.stringify(response, null, 2));
      }
      return { content: content };
    } catch (parseError) {
      console.error('Error parsing JSON response:', parseError);
      return { error: 'Failed to parse response from backend' };
    }
  } catch (error) {
    console.error('Error sending message:', error);
    return { error: error.message || 'Unknown error' };
  }
}

export async function uploadFile(formData) {
  try {
    const res = await fetch(`${API_BASE}/chat/upload`, {
      method: 'POST',
      body: formData
    });
    const response = await res.json();
    return response || { error: 'Unknown error' };
  } catch (error) {
    console.error('Error uploading file:', error);
    return { error: error.message || 'Unknown error' };
  }
}

// Function to handle streaming responses (to be implemented on backend)
export function streamMessage({ provider, model, messages, options, onChunk }) {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`${API_BASE}/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, model, messages, options })
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const reader = res.body.getReader();
      let fullResponse = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          resolve({ content: fullResponse });
          break;
        }
        
        const chunk = new TextDecoder('utf-8').decode(value);
        fullResponse += chunk;
        onChunk(chunk);
      }
    } catch (error) {
      console.error('Error streaming message:', error);
      reject(error);
    }
  });
}
