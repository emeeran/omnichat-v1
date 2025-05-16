import React, { useState } from 'react';
import '@styles/App.css';
import ChatWindow from './components/ChatWindow';
import SettingsSidebar from './components/SettingsSidebar';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [provider, setProvider] = useState('openai');
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [persona, setPersona] = useState('Default');
  const [chatHistory, setChatHistory] = useState([]);
  const [savedChats, setSavedChats] = useState([]);
  const [textSize, setTextSize] = useState('Medium');
  const [themeColor, setThemeColor] = useState('Default');

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    // Ensure the entire document root reflects the mode change
    document.documentElement.className = newDarkMode ? 'dark-mode' : 'light-mode';
    // Also update body for additional compatibility
    document.body.className = newDarkMode ? 'dark-mode' : 'light-mode';
  };

  const [retryTrigger, setRetryTrigger] = useState(0);

  const handleRetry = () => {
    // Retry the last user query with the current model
    if (chatHistory.length > 0) {
      // Find the last user message
      const lastUserQuery = [...chatHistory].reverse().find(msg => msg.sender === 'user');
      if (lastUserQuery) {
        alert(`Retrying last query: "${lastUserQuery.text.substring(0, 30)}..." with model: ${model}`);
        setRetryTrigger(prev => prev + 1); // Trigger retry in ChatWindow
      } else {
        alert('No user query found to retry. Please ensure you have sent a message.');
      }
    } else {
      alert('No chat history to retry. Please send a message first.');
    }
  };

  const handleNewChat = () => {
    // Refresh both query and response by clearing the chat history
    setChatHistory([]);
    alert('Starting a new chat session. Previous queries and responses have been deleted.');
  };

  const handleSaveChat = () => {
    // Save current chat for later retrieval
    const chatName = prompt('Enter a name for this chat:');
    if (chatName) {
      const newSavedChat = { name: chatName, history: [...chatHistory] };
      setSavedChats([...savedChats, newSavedChat]);
      alert(`Chat saved as "${chatName}".`);
    }
  };

  const handleLoadChat = () => {
    // Load a selected chat from saved chats
    if (savedChats.length === 0) {
      alert('No saved chats to load.');
      return;
    }
    const chatNames = savedChats.map(chat => chat.name).join(', ');
    const selectedName = prompt(`Enter the name of the chat to load (${chatNames}):`);
    const selectedChat = savedChats.find(chat => chat.name === selectedName);
    if (selectedChat) {
      setChatHistory([...selectedChat.history]);
      alert(`Loaded chat "${selectedName}".`);
    } else {
      alert('Chat not found.');
    }
  };

  const handleDeleteChat = () => {
    // Delete a selected chat
    if (savedChats.length === 0) {
      alert('No saved chats to delete.');
      return;
    }
    const chatNames = savedChats.map(chat => chat.name).join(', ');
    const selectedName = prompt(`Enter the name of the chat to delete (${chatNames}):`);
    const updatedChats = savedChats.filter(chat => chat.name !== selectedName);
    setSavedChats(updatedChats);
    alert(`Deleted chat "${selectedName}".`);
  };

  const handleExportChat = () => {
    // Export chat history to various formats
    if (chatHistory.length === 0) {
      alert('No chat history to export.');
      return;
    }
    const format = prompt('Enter export format (txt, json):');
    if (format) {
      let content = '';
      let mimeType = '';
      if (format === 'txt') {
        content = chatHistory.map(msg => `${msg.sender}: ${msg.text}`).join('\n');
        mimeType = 'text/plain';
      } else if (format === 'json') {
        content = JSON.stringify(chatHistory, null, 2);
        mimeType = 'application/json';
      } else {
        alert('Unsupported format. Use txt or json.');
        return;
      }
      const blob = new Blob([content], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `chat_history.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      alert(`Chat history exported as ${format}.`);
    }
  };

  // Apply theme color as a CSS variable
  const themeColorValue = themeColor === 'Green' ? '#00BFA5' : themeColor === 'Purple' ? '#9C27B0' : themeColor === 'Orange' ? '#FF9800' : themeColor === 'Teal' ? '#009688' : themeColor === 'Red' ? '#F44336' : themeColor === 'Indigo' ? '#3F51B5' : themeColor === 'Amber' ? '#FFC107' : '#3B82F6';
  document.documentElement.style.setProperty('--primary-color', themeColorValue);
  document.documentElement.style.setProperty('--primary-dark', themeColor === 'Green' ? '#008C7A' : themeColor === 'Purple' ? '#7E1F86' : themeColor === 'Orange' ? '#E65100' : themeColor === 'Teal' ? '#00796B' : themeColor === 'Red' ? '#D32F2F' : themeColor === 'Indigo' ? '#303F9F' : themeColor === 'Amber' ? '#FFA000' : '#2563EB');

  // Apply text size as a CSS variable
  const textSizeValue = textSize === 'Small' ? '0.8em' : textSize === 'Large' ? '1.2em' : '1em';
  document.documentElement.style.setProperty('--base-font-size', textSizeValue);

  return (
    <div className={`app-container ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <main className="app-main">
        <div className="content-wrapper">
          <SettingsSidebar
            provider={provider}
            setProvider={setProvider}
            model={model}
            setModel={setModel}
            persona={persona}
            setPersona={setPersona}
            onRetry={handleRetry}
            onNewChat={handleNewChat}
            onSaveChat={handleSaveChat}
            onLoadChat={handleLoadChat}
            onDeleteChat={handleDeleteChat}
            onExportChat={handleExportChat}
            darkMode={darkMode}
            toggleDarkMode={toggleDarkMode}
            textSize={textSize}
            setTextSize={setTextSize}
            themeColor={themeColor}
            setThemeColor={setThemeColor}
          />
          <ChatWindow provider={provider} model={model} persona={persona} chatHistory={chatHistory} setChatHistory={setChatHistory} retryTrigger={retryTrigger} textSize={textSize} themeColor={themeColor} />
        </div>
      </main>
    </div>
  );
}
