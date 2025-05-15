import React from 'react';
import ProviderModelSelector from './ProviderModelSelector';

export default function ChatManagementBar({ provider, setProvider, model, setModel, onRetry, onNewChat, onSaveChat, onLoadChat, onDeleteChat, onExportChat }) {
  const handleProviderChange = (value) => {
    setProvider(value);
    setModel(''); // Reset model when provider changes
  };

  const handleModelChange = (value) => {
    setModel(value);
  };

  return (
    <div className="chat-management-bar">
      <div className="provider-model-section">
        <ProviderModelSelector
          provider={provider}
          model={model}
          onProviderChange={handleProviderChange}
          onModelChange={handleModelChange}
        />
        <div className="current-selection">
          {provider && model ? `${provider} | ${model}` : 'Select Provider & Model'}
        </div>
      </div>
      <div className="chat-buttons-section">
        <button onClick={onNewChat} className="chat-action-btn" aria-label="Start a new chat">New</button>
        <button onClick={onRetry} className="chat-action-btn" aria-label="Retry the last action">Retry</button>
        <button onClick={onSaveChat} className="chat-action-btn" aria-label="Save current chat">Save</button>
        <button onClick={onLoadChat} className="chat-action-btn" aria-label="Load a saved chat">Load</button>
        <button onClick={onDeleteChat} className="chat-action-btn" aria-label="Delete a saved chat">Delete</button>
        <button onClick={onExportChat} className="chat-action-btn" aria-label="Export current chat">Export</button>
      </div>
    </div>
  );
}