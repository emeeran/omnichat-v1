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

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.className = darkMode ? 'light-mode' : 'dark-mode';
  };

  const handleRetry = () => {
    // Retry the last query with a different provider/model
    if (chatHistory.length > 0) {
      const lastQuery = chatHistory[chatHistory.length - 1];
      // Placeholder: Logic to retry with different provider/model
      alert('Retrying last query with different provider/model. This functionality needs backend integration.');
      setChatHistory([...chatHistory, { ...lastQuery, retry: true }]);
    } else {
      alert('No previous query to retry.');
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
    const format = prompt('Enter export format (md, pdf, json, txt):');
    if (format) {
      // Placeholder: Logic to export chat history in the selected format
      alert(`Exporting chat history to ${format}. This functionality needs backend integration or file download implementation.`);
    }
  };

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
          />
          <ChatWindow provider={provider} model={model} persona={persona} chatHistory={chatHistory} setChatHistory={setChatHistory} />
        </div>
      </main>
    </div>
  );
}
