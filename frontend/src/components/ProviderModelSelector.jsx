// src/components/ProviderModelSelector.jsx
import React, { useEffect, useState } from 'react';
import { fetchProviders, fetchModels } from '../services/api';

export default function ProviderModelSelector({
  provider, model, onProviderChange, onModelChange
}) {
  const [providers, setProviders] = useState([]);
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadProviders = async () => {
      setLoading(true);
      const providersData = await fetchProviders();
      if (providersData && providersData.length > 0) {
        setProviders(providersData);
      } else {
        // Fallback to static data if API call fails or returns empty
        setProviders([
          { id: 'openai', name: 'OpenAI' },
          { id: 'anthropic', name: 'Anthropic' },
          { id: 'google', name: 'Google' }
        ]);
      }
      setLoading(false);
    };
    loadProviders();
  }, []);

  useEffect(() => {
    const loadModels = async () => {
      if (provider) {
        setLoading(true);
        const modelsData = await fetchModels(provider);
        if (modelsData && modelsData.length > 0) {
          setModels(modelsData);
          // Set default model for OpenAI if no model is selected
          if (provider.toLowerCase() === 'openai' && !model) {
            onModelChange('gpt-4.1-nano-2025-04-14');
          }
        } else {
          // Fallback to static data based on provider if API call fails or returns empty
          const fallbackModels = {
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
            ]
          };
          setModels(fallbackModels[provider.toLowerCase()] || []);
          // Set default model for OpenAI if no model is selected
          if (provider.toLowerCase() === 'openai' && !model) {
            onModelChange('gpt-4.1-nano-2025-04-14');
          }
        }
        setLoading(false);
      } else {
        setModels([]);
      }
    };
    loadModels();
  }, [provider, model, onModelChange]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        <label style={{ fontSize: '0.95rem', fontWeight: '500' }}>Provider:</label>
        <select
          value={provider || ''}
          onChange={e => onProviderChange(e.target.value)}
        >
          <option value='' disabled>Select a Provider</option>
          {providers.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        <label style={{ fontSize: '0.95rem', fontWeight: '500' }}>Model:</label>
        <select
          value={model || ''}
          onChange={e => onModelChange(e.target.value)}
          disabled={!provider || loading}
        >
          <option value='' disabled>
            {loading ? 'Loading models...' : provider ? 'Select a Model' : 'Select Provider First'}
          </option>
          {models.map(m => (
            <option key={m.id || m} value={m.id || m}>
              {m.name || m.id || m}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
