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

export default function SettingsSidebar({ provider, setProvider, model, setModel, persona, setPersona, onRetry, onNewChat, onSaveChat, onLoadChat, onDeleteChat, onExportChat, darkMode, toggleDarkMode, textSize, setTextSize, themeColor, setThemeColor }) {
  const [mode, setMode] = useState('chat');
  const [maxTemp, setMaxTemp] = useState(1.0);
  const [temp, setTemp] = useState(0.7);
  const [audioResponse, setAudioResponse] = useState(false);
  const [localTextSize, setLocalTextSize] = useState('Medium');
  const [localThemeColor, setLocalThemeColor] = useState('Default');
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

  // Load default settings on component mount
  React.useEffect(() => {
    const savedSettings = JSON.parse(localStorage.getItem('defaultSettings') || '{}');
    if (savedSettings.provider) setProvider(savedSettings.provider);
    if (savedSettings.model) setModel(savedSettings.model);
    if (savedSettings.persona) setPersona(savedSettings.persona);
    if (savedSettings.mode) setMode(savedSettings.mode);
    if (savedSettings.temp !== undefined) setTemp(savedSettings.temp);
    if (savedSettings.maxTemp !== undefined) setMaxTemp(savedSettings.maxTemp);
    if (savedSettings.audioResponse !== undefined) setAudioResponse(savedSettings.audioResponse);
    if (savedSettings.darkMode !== undefined && darkMode !== savedSettings.darkMode) toggleDarkMode();
    if (savedSettings.textSize) {
      setLocalTextSize(savedSettings.textSize);
      setTextSize(savedSettings.textSize);
    }
    if (savedSettings.themeColor) {
      setLocalThemeColor(savedSettings.themeColor);
      setThemeColor(savedSettings.themeColor);
    }
  }, [darkMode, setProvider, setModel, setPersona, toggleDarkMode, setTextSize, setThemeColor]);

  return (
    <div className="settings-sidebar">
      <div className="settings-drawer compact-drawer always-open">
        <div className="settings-tabs" role="tablist">
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
                <div style={{ fontSize: '0.8em', color: '#888', marginTop: '5px' }}>Enable audio playback for AI responses</div>
              </div>
              <div className="settings-group compact-group">
                <label>Save Settings</label>
                <button onClick={() => {
                  const settings = {
                    provider,
                    model,
                    persona,
                    mode,
                    temp,
                    maxTemp,
                    audioResponse,
                    darkMode,
                    textSize: localTextSize,
                    themeColor: localThemeColor
                  };
                  localStorage.setItem('defaultSettings', JSON.stringify(settings));
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
                <select id="text-size-select" value={localTextSize} onChange={e => {
                  setLocalTextSize(e.target.value);
                  setTextSize(e.target.value);
                }}>
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
                <select id="theme-color-select" value={localThemeColor} onChange={e => {
                  setLocalThemeColor(e.target.value);
                  setThemeColor(e.target.value);
                }}>
                  <option value="Default">Default (Blue)</option>
                  <option value="Green">Green</option>
                  <option value="Purple">Purple</option>
                  <option value="Orange">Orange</option>
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
    </div>
  );
}
