import React, { useState } from 'react';
import ProviderModelSelector from './ProviderModelSelector';

async function registerProvider(providerId, apiKey) {
  try {
    const res = await fetch('/api/providers/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider_id: providerId, api_key: apiKey })
    });
    const response = await res.json();
    return response.success ? { success: true } : { error: response.error || 'Failed to register provider' };
  } catch (error) {
    console.error('Error registering provider:', error);
    return { error: error.message || 'Unknown error' };
  }
}

export default function SettingsSidebar({ provider, setProvider, model, setModel, persona, setPersona, onRetry, onNewChat, onSaveChat, onLoadChat, onDeleteChat, onExportChat, darkMode, toggleDarkMode }) {
  const [mode, setMode] = useState('chat');
  const [maxTemp, setMaxTemp] = useState(1.0);
  const [temp, setTemp] = useState(0.7);
  const [audioResponse, setAudioResponse] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [apiKeyError, setApiKeyError] = useState('');
  const [apiKeySuccess, setApiKeySuccess] = useState(false);

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  const handleProviderChange = (value) => {
    setProvider(value);
    setModel(''); // Reset model when provider changes
  };

  const handleModelChange = (value) => {
    setModel(value);
  };

  const handlePersonaChange = (e) => {
    setPersona(e.target.value);
  };

  const handleApiKeySubmit = async () => {
    if (!provider) {
      setApiKeyError('Please select a provider first');
      return;
    }
    if (!apiKey.trim()) {
      setApiKeyError('API key cannot be empty');
      return;
    }
    setApiKeyError('');
    const result = await registerProvider(provider, apiKey);
    if (result.success) {
      setApiKeySuccess(true);
      setApiKey('');
      setTimeout(() => setApiKeySuccess(false), 3000);
    } else {
      setApiKeyError(result.error || 'Failed to register provider');
    }
  };

  return (
    <div className="settings-sidebar">
      <button onClick={toggleDrawer} className="drawer-toggle-button" aria-label="Toggle Settings Drawer">
        <span className="toggle-icon">⚙️</span>
        SETTINGS
      </button>
      {isDrawerOpen && (
        <div className="settings-drawer">
          <div className="settings-group">
            <label>Mode:</label>
            <select value={mode} onChange={(e) => setMode(e.target.value)}>
              <option value="" disabled>Select Mode</option>
              <option value="chat">Chat</option>
              <option value="assistant">Assistant</option>
              <option value="code">Code</option>
            </select>
          </div>
          <div className="settings-group">
            <ProviderModelSelector 
              provider={provider} 
              model={model} 
              onProviderChange={handleProviderChange} 
              onModelChange={handleModelChange} 
            />
          </div>
          <div className="settings-group">
            <label>Persona:</label>
            <select value={persona} onChange={handlePersonaChange}>
              <option value="" disabled>Select Persona</option>
              <option value="Default">Default</option>
              <option value="Technical">Technical</option>
              <option value="Friendly">Friendly</option>
            </select>
          </div>
          <div className="settings-group slider-group">
            <label>Max Tokens: {maxTemp.toFixed(0)}</label>
            <input 
              type="range" 
              min="0" 
              max="4096" 
              step="64" 
              value={maxTemp} 
              onChange={(e) => setMaxTemp(parseFloat(e.target.value))} 
            />
          </div>
          <div className="settings-group slider-group">
            <label>Temperature: {temp.toFixed(1)}</label>
            <input 
              type="range" 
              min="0" 
              max="2" 
              step="0.1" 
              value={temp} 
              onChange={(e) => setTemp(parseFloat(e.target.value))} 
            />
          </div>
          <div className="settings-group">
            <label>Theme:</label>
            <button onClick={toggleDarkMode} className="theme-toggle-button">
              {darkMode ? 'Light Mode' : 'Dark Mode'}
            </button>
          </div>
          <div className="settings-group">
            <label>Configure API Key for {provider || 'Selected Provider'}:</label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter API Key"
              disabled={!provider}
            />
            <button onClick={handleApiKeySubmit} disabled={!provider || !apiKey.trim()}>
              Register API Key
            </button>
            {apiKeyError && <p className="error-message">{apiKeyError}</p>}
            {apiKeySuccess && <p className="success-message">API Key registered successfully!</p>}
          </div>
        </div>
      )}
      <div className="settings-buttons">
        <div className="button-row">
          <button onClick={onRetry}>Retry</button>
          <button onClick={onNewChat}>New</button>
          <button onClick={onSaveChat}>Save</button>
        </div>
        <div className="button-row">
          <button onClick={onLoadChat}>Load</button>
          <button onClick={onDeleteChat}>Delete</button>
          <button onClick={onExportChat}>Export</button>
        </div>
      </div>
      <div className="settings-group radio-group">
        <label>
          <input 
            type="radio" 
            checked={audioResponse} 
            onChange={() => setAudioResponse(!audioResponse)} 
          />
          Audio Response
        </label>
      </div>
      <div className="settings-footer">
        {provider && model ? `${provider} | ${model}` : 'No selection'}
      </div>
    </div>
  );
}
