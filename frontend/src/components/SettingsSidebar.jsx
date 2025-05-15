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
  const [apiKey, setApiKey] = useState('');
  const [apiKeyError, setApiKeyError] = useState('');
  const [apiKeySuccess, setApiKeySuccess] = useState(false);

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

  const [activeTab, setActiveTab] = useState('provider');

  const handleTabKeyDown = (e, tabName) => {
    const tabs = ['provider', 'chat', 'advanced', 'appearance'];
    const currentIndex = tabs.indexOf(activeTab);
    let newIndex = currentIndex;

    if (e.key === 'ArrowLeft') {
      newIndex = (currentIndex - 1 + tabs.length) % tabs.length;
    } else if (e.key === 'ArrowRight') {
      newIndex = (currentIndex + 1) % tabs.length;
    } else if (e.key === 'Enter' || e.key === ' ') {
      setActiveTab(tabName);
      return;
    } else {
      return;
    }

    setActiveTab(tabs[newIndex]);
    e.preventDefault();
  };

  return (
    <div className="settings-sidebar">
      <div className="settings-drawer compact-drawer always-open">
        <div className="settings-tabs" role="tablist">
          <button
            className={`tab-button ${activeTab === 'provider' ? 'active' : ''}`}
            onClick={() => setActiveTab('provider')}
            onKeyDown={(e) => handleTabKeyDown(e, 'provider')}
            aria-selected={activeTab === 'provider'}
            role="tab"
            id="provider-tab"
            aria-controls="provider-panel"
            tabIndex={activeTab === 'provider' ? 0 : -1}
          >
            Provider
          </button>
          <button
            className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
            onKeyDown={(e) => handleTabKeyDown(e, 'chat')}
            aria-selected={activeTab === 'chat'}
            role="tab"
            id="chat-tab"
            aria-controls="chat-panel"
            tabIndex={activeTab === 'chat' ? 0 : -1}
          >
            Chat
          </button>
          <button
            className={`tab-button ${activeTab === 'advanced' ? 'active' : ''}`}
            onClick={() => setActiveTab('advanced')}
            onKeyDown={(e) => handleTabKeyDown(e, 'advanced')}
            aria-selected={activeTab === 'advanced'}
            role="tab"
            id="advanced-tab"
            aria-controls="advanced-panel"
            tabIndex={activeTab === 'advanced' ? 0 : -1}
          >
            Advanced
          </button>
          <button
            className={`tab-button ${activeTab === 'appearance' ? 'active' : ''}`}
            onClick={() => setActiveTab('appearance')}
            onKeyDown={(e) => handleTabKeyDown(e, 'appearance')}
            aria-selected={activeTab === 'appearance'}
            role="tab"
            id="appearance-tab"
            aria-controls="appearance-panel"
            tabIndex={activeTab === 'appearance' ? 0 : -1}
          >
            Appearance
          </button>
        </div>
        <div className="settings-content">
          {activeTab === 'provider' && (
            <div className="settings-category" role="tabpanel" id="provider-panel" aria-labelledby="provider-tab">
              <h3>Provider Settings</h3>
              <div className="settings-group compact-group">
                <ProviderModelSelector
                  provider={provider}
                  model={model}
                  onProviderChange={handleProviderChange}
                  onModelChange={handleModelChange}
                />
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="api-key-input">API Key</label>
                <input
                  id="api-key-input"
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Enter API Key"
                  className="api-key-input"
                  aria-describedby={apiKeyError ? "api-key-error" : apiKeySuccess ? "api-key-success" : ""}
                />
                <button onClick={handleApiKeySubmit} className="api-key-submit" disabled={!apiKey.trim() || !provider}>Register</button>
                {apiKeyError && <div className="error-message" id="api-key-error">{apiKeyError}</div>}
                {apiKeySuccess && <div className="success-message" id="api-key-success">API Key registered successfully!</div>}
              </div>
            </div>
          )}
          {activeTab === 'chat' && (
            <div className="settings-category" role="tabpanel" id="chat-panel" aria-labelledby="chat-tab">
              <h3>Chat Settings</h3>
              <div className="settings-group compact-group">
                <label htmlFor="mode-select">Mode</label>
                <select id="mode-select" value={mode} onChange={e => setMode(e.target.value)}>
                  <option value="chat">Chat</option>
                  <option value="assistant">Assistant</option>
                  <option value="code">Code</option>
                </select>
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="persona-select">Persona</label>
                <select id="persona-select" value={persona} onChange={handlePersonaChange}>
                  <option value="Default">Default</option>
                  <option value="Technical">Technical</option>
                  <option value="Friendly">Friendly</option>
                </select>
              </div>
              <div className="settings-group chat-management compact-group">
                <label>Chat Management</label>
                <div className="chat-buttons compact-buttons">
                  <button onClick={onNewChat} className="chat-action-btn">New</button>
                  <button onClick={onRetry} className="chat-action-btn">Retry</button>
                  <button onClick={onSaveChat} className="chat-action-btn">Save</button>
                  <button onClick={onLoadChat} className="chat-action-btn">Load</button>
                  <button onClick={onDeleteChat} className="chat-action-btn">Delete</button>
                  <button onClick={onExportChat} className="chat-action-btn">Export</button>
                </div>
              </div>
            </div>
          )}
          {activeTab === 'advanced' && (
            <div className="settings-category" role="tabpanel" id="advanced-panel" aria-labelledby="advanced-tab">
              <h3>Advanced Settings</h3>
              <div className="settings-group slider-group compact-group">
                <div style={{display: 'flex', justifyContent: 'space-between', width: '100%'}}>
                  <label htmlFor="max-tokens-slider">Max Tokens</label>
                  <span style={{fontSize: '0.85em', color: '#888'}}>{maxTemp}</span>
                </div>
                <input
                  id="max-tokens-slider"
                  type="range"
                  min="0"
                  max="4096"
                  step="64"
                  value={maxTemp}
                  onChange={(e) => setMaxTemp(parseFloat(e.target.value))}
                  className="settings-slider"
                />
              </div>
              <div className="settings-group slider-group compact-group">
                <div style={{display: 'flex', justifyContent: 'space-between', width: '100%'}}>
                  <label htmlFor="temperature-slider">Temp</label>
                  <span style={{fontSize: '0.85em', color: '#888'}}>{temp}</span>
                </div>
                <input
                  id="temperature-slider"
                  type="range"
                  min="0"
                  max="2"
                  step="0.1"
                  value={temp}
                  onChange={(e) => setTemp(parseFloat(e.target.value))}
                  className="settings-slider"
                />
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="audio-response-checkbox">Audio Response</label>
                <input
                  id="audio-response-checkbox"
                  type="checkbox"
                  checked={audioResponse}
                  onChange={() => setAudioResponse(!audioResponse)}
                />
              </div>
            </div>
          )}
          {activeTab === 'appearance' && (
            <div className="settings-category" role="tabpanel" id="appearance-panel" aria-labelledby="appearance-tab">
              <h3>Appearance</h3>
              <div className="settings-group compact-group">
                <label htmlFor="dark-mode-toggle">Dark Mode</label>
                <input
                  id="dark-mode-toggle"
                  type="checkbox"
                  checked={darkMode}
                  onChange={toggleDarkMode}
                />
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="settings-footer">
        {provider && model ? `${provider} | ${model}` : ''}
      </div>
    </div>
  );
}
