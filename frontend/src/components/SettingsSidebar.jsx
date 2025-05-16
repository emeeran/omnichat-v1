import React, { useState } from 'react';
import ProviderModelSelector from './ProviderModelSelector';

const SettingsSidebar = ({ provider, setProvider, model, setModel, persona, setPersona, onRetry, onNewChat, onSaveChat, onLoadChat, onDeleteChat, onExportChat, darkMode, toggleDarkMode, textSize, setTextSize, themeColor, setThemeColor }) => {
  const [settings, setSettings] = useState({
    mode: 'chat',
    maxTemp: 1.0,
    temp: 0.7,
    audioResponse: false,
    textSize: 'Medium',
    themeColor: 'Default'
  });
  const [apiKey, setApiKey] = useState('');
  const [apiKeyError, setApiKeyError] = useState('');
  const [apiKeySuccess, setApiKeySuccess] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState('provider');

  const tabs = [
    { id: 'provider', emoji: '🌐' },
    { id: 'chat', emoji: '💬' },
    { id: 'advanced', emoji: '⚙️' },
    { id: 'appearance', emoji: '🎨' }
  ];

  const toggleCollapse = () => {
    setCollapsed(!collapsed);
  };

  const handleTabKeyDown = (e, tabId) => {
    if (e.key === 'Enter') {
      setActiveTab(tabId);
    }
  };

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

  const updateSettings = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleProviderOrModelChange = (type, value) => {
    if (type === 'provider') {
      setProvider(value);
      setModel(''); // Reset model when provider changes
    } else if (type === 'model') {
      setModel(value);
    }
  };

  const handlePersonaChange = (e) => {
    setPersona(e.target.value);
  };

  const handleSettingChange = (key) => (e) => {
    updateSettings(key, e.target.value);
    if (key === 'textSize') setTextSize(e.target.value);
    if (key === 'themeColor') setThemeColor(e.target.value);
  };

  const toggleAudioResponse = () => {
    updateSettings('audioResponse', !settings.audioResponse);
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
    <div className={`settings-sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="settings-drawer compact-drawer always-open">
        <div className="settings-tabs" role="tablist">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
              onKeyDown={(e) => handleTabKeyDown(e, tab.id)}
              aria-selected={activeTab === tab.id}
              role="tab"
              id={`${tab.id}-tab`}
              aria-controls={`${tab.id}-panel`}
              tabIndex={activeTab === tab.id ? 0 : -1}
            >
              {tab.emoji}
            </button>
          ))}
        </div>
        <div className="settings-content">
          {activeTab === 'provider' && (
            <div className="settings-category" role="tabpanel" id="provider-panel" aria-labelledby="provider-tab">
              <h3>Provider Settings</h3>
              <div className="settings-group compact-group">
                <ProviderModelSelector
                  provider={provider}
                  model={model}
                  onProviderChange={(value) => handleProviderOrModelChange('provider', value)}
                  onModelChange={(value) => handleProviderOrModelChange('model', value)}
                />
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="api-key-input">API Key</label>
                <form onSubmit={(e) => e.preventDefault()}>
                  <input
                    id="api-key-input"
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="Enter API Key"
                    className="api-key-input"
                    aria-describedby={apiKeyError ? "api-key-error" : apiKeySuccess ? "api-key-success" : ""}
                    autoComplete="new-password"
                  />
                  <button onClick={handleApiKeySubmit} className="api-key-submit" disabled={!apiKey.trim() || !provider}>Register</button>
                </form>
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
                <select id="mode-select" value={settings.mode} onChange={handleSettingChange('mode')}>
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
            </div>
          )}
          {activeTab === 'advanced' && (
            <div className="settings-category" role="tabpanel" id="advanced-panel" aria-labelledby="advanced-tab">
              <h3>Advanced Settings</h3>
              <div className="settings-group slider-group compact-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                  <label htmlFor="max-tokens-slider">Max Tokens</label>
                  <span style={{ fontSize: '0.85em', color: '#888' }}>{settings.maxTemp}</span>
                </div>
                <input
                  id="max-tokens-slider"
                  type="range"
                  min="0"
                  max="4096"
                  step="64"
                  value={settings.maxTemp}
                  onChange={(e) => updateSettings('maxTemp', parseFloat(e.target.value))}
                  className="settings-slider"
                />
              </div>
              <div className="settings-group slider-group compact-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                  <label htmlFor="temperature-slider">Temp</label>
                  <span style={{ fontSize: '0.85em', color: '#888' }}>{settings.temp}</span>
                </div>
                <input
                  id="temperature-slider"
                  type="range"
                  min="0"
                  max="2"
                  step="0.1"
                  value={settings.temp}
                  onChange={(e) => updateSettings('temp', parseFloat(e.target.value))}
                  className="settings-slider"
                />
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="audio-response-checkbox">Audio Response</label>
                <input
                  id="audio-response-checkbox"
                  type="checkbox"
                  checked={settings.audioResponse}
                  onChange={toggleAudioResponse}
                />
                <div style={{ fontSize: '0.8em', color: '#888', marginTop: '5px' }}>Enable audio playback for AI responses</div>
              </div>
              <div className="settings-group compact-group">
                <label>Save Settings</label>
                <button onClick={() => {
                  const combinedSettings = {
                    provider,
                    model,
                    persona,
                    darkMode,
                    ...settings
                  };
                  localStorage.setItem('defaultSettings', JSON.stringify(combinedSettings));
                  alert('Settings saved as default!');
                }} className="save-default-btn" aria-label="Save current settings as default" style={{ marginTop: '5px', width: '100%', padding: '8px' }}>Save as Default</button>
                <div style={{ fontSize: '0.8em', color: '#888', marginTop: '5px' }}>Saves current settings for future sessions</div>
              </div>
            </div>
          )}
          {activeTab === 'appearance' && (
            <div className="settings-category" role="tabpanel" id="appearance-panel" aria-labelledby="appearance-tab">
              <h3>Appearance Settings</h3>
              <div className="settings-group compact-group">
                <label>Theme Mode</label>
                <button onClick={toggleDarkMode} className="theme-toggle-btn" aria-label="Toggle dark/light mode">
                  {darkMode ? 'Light Mode' : 'Dark Mode'}
                </button>
                <div style={{ fontSize: '0.8em', color: '#888', marginTop: '5px' }}>
                  Switch to {darkMode ? 'light' : 'dark'} mode for a different visual experience
                </div>
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="text-size-select">Text Size</label>
                <select id="text-size-select" value={settings.textSize} onChange={handleSettingChange('textSize')}>
                  <option value="Small">Small</option>
                  <option value="Medium">Medium</option>
                  <option value="Large">Large</option>
                </select>
                <div style={{ fontSize: '0.8em', color: '#888', marginTop: '5px' }}>
                  Adjust the size of text in the application
                </div>
              </div>
              <div className="settings-group compact-group">
                <label htmlFor="theme-color-select">Theme Color</label>
                <select id="theme-color-select" value={settings.themeColor} onChange={handleSettingChange('themeColor')}>
                  <option value="Default">Default (Blue)</option>
                  <option value="Green">Green</option>
                  <option value="Purple">Purple</option>
                  <option value="Orange">Orange</option>
                  <option value="Teal">Teal</option>
                  <option value="Red">Red</option>
                  <option value="Indigo">Indigo</option>
                  <option value="Amber">Amber</option>
                </select>
                <div style={{ fontSize: '0.8em', color: '#888', marginTop: '5px' }}>
                  Choose a primary color theme for the application
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="settings-footer">
        <div className="chat-management-buttons">
          <button onClick={onNewChat} className="chat-action-btn" aria-label="Start a new chat">New</button>
          <button onClick={onRetry} className="chat-action-btn" aria-label="Retry the last action">Retry</button>
          <button onClick={onSaveChat} className="chat-action-btn" aria-label="Save current chat">Save</button>
          <button onClick={onLoadChat} className="chat-action-btn" aria-label="Load a saved chat">Load</button>
          <button onClick={onDeleteChat} className="chat-action-btn" aria-label="Delete a saved chat">Delete</button>
          <button onClick={onExportChat} className="chat-action-btn" aria-label="Export current chat">Export</button>
        </div>
      </div>
      <button onClick={toggleCollapse} className="collapse-toggle-btn" aria-label="Toggle sidebar collapse">
        {collapsed ? 'Expand' : 'Collapse'}
      </button>
    </div>
  );
};

export default SettingsSidebar;
