import React, { useState } from 'react';
import '@styles/ChatWindow.css';
import '@styles/Markdown.css';

const ChatWindow = ({ provider, model, persona, chatHistory, setChatHistory, retryTrigger, textSize, themeColor }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Sync messages with chatHistory from parent
  React.useEffect(() => {
    setMessages(chatHistory);
  }, [chatHistory]);

  // Handle retry trigger
  React.useEffect(() => {
    if (retryTrigger > 0) {
      const lastUserQuery = [...messages].reverse().find(msg => msg.sender === 'user');
      if (lastUserQuery) {
        handleRetryMessage(lastUserQuery);
      }
    }
  }, [retryTrigger]);

  const handleRetryMessage = async (query) => {
    const retryMessage = {
      id: Date.now(),
      text: query.text + " (Retry)",
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
      isRetry: true
    };
    const updatedMessages = [...messages, retryMessage];
    setMessages(updatedMessages);
    setChatHistory(updatedMessages);
    
    // Send message to backend for AI response
    try {
      const { sendMessage } = await import('../services/api.js');
      const response = await sendMessage({
        provider: provider,
        model: model,
        messages: updatedMessages.map(msg => ({ role: msg.sender === 'user' ? 'user' : 'assistant', content: msg.text })),
        options: {}
      });
      if (response.error) {
        let errorText = `Error: ${response.error}`;
        if (response.error.includes("Provider not configured")) {
          errorText = "Error: Provider not configured. Please ensure an API key is set up for the selected provider in the backend.";
        }
        const errorResponse = {
          id: Date.now() + 1,
          text: errorText,
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString(),
        };
        const newMessages = [...updatedMessages, errorResponse];
        setMessages(newMessages);
        setChatHistory(newMessages);
      } else {
        const aiResponse = {
          id: Date.now() + 1,
          text: response.content || 'No response content',
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString(),
          isRetryResponse: true
        };
        const newMessages = [...updatedMessages, aiResponse];
        setMessages(newMessages);
        setChatHistory(newMessages);
      }
    } catch (error) {
      const errorResponse = {
        id: Date.now() + 1,
        text: `Error sending message: ${error.message}`,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString(),
      };
      const newMessages = [...updatedMessages, errorResponse];
      setMessages(newMessages);
      setChatHistory(newMessages);
    }
  };

  const handleSendMessage = async () => {
    if (input.trim()) {
      const newMessage = {
        id: Date.now(),
        text: input,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString(),
      };
      const updatedMessages = [...messages, newMessage];
      setMessages(updatedMessages);
      setChatHistory(updatedMessages);
      setInput('');
      
      // Send message to backend for AI response
      try {
        const { sendMessage } = await import('../services/api.js');
        const response = await sendMessage({
          provider: provider,
          model: model,
          messages: [...messages, newMessage].map(msg => ({ role: msg.sender === 'user' ? 'user' : 'assistant', content: msg.text })),
          options: {}
        });
        if (response.error) {
          let errorText = `Error: ${response.error}`;
          if (response.error.includes("Provider not configured")) {
            errorText = "Error: Provider not configured. Please ensure an API key is set up for the selected provider in the backend.";
          }
          const errorResponse = {
            id: Date.now() + 1,
            text: errorText,
            sender: 'ai',
            timestamp: new Date().toLocaleTimeString(),
          };
          const updatedMessages = [...messages, errorResponse];
          setMessages(updatedMessages);
          setChatHistory(updatedMessages);
        } else {
          const aiResponse = {
            id: Date.now() + 1,
            text: response.content || 'No response content',
            sender: 'ai',
            timestamp: new Date().toLocaleTimeString(),
          };
          const updatedMessages = [...messages, aiResponse];
          setMessages(updatedMessages);
          setChatHistory(updatedMessages);
        }
      } catch (error) {
        const errorResponse = {
          id: Date.now() + 1,
          text: `Error sending message: ${error.message}`,
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString(),
        };
        const updatedMessages = [...messages, errorResponse];
        setMessages(updatedMessages);
        setChatHistory(updatedMessages);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Simple Markdown to HTML converter for basic formatting
  const simpleMarkdownToHtml = (text) => {
    let html = text
      // Escape HTML to prevent XSS
      .replace(/</g, '<')
      .replace(/>/g, '>')
      // Bold: **text** or __text__
      .replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/__([^_]+)__/g, '<strong>$1</strong>')
      // Italic: *text* or _text_
      .replace(/\*([^\*]+)\*/g, '<em>$1</em>')
      .replace(/_([^_]+)_/g, '<em>$1</em>')
      // Inline code: `code`
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      // Code block: ```language ... ```
      .replace(/```(\w*)\n([\s\S]*?)\n```/g, '<pre><code class="language-$1">$2</code></pre>')
      // Headings: # Heading, ## Heading, etc.
      .replace(/^###### (.*)$/gm, '<h6>$1</h6>')
      .replace(/^##### (.*)$/gm, '<h5>$1</h5>')
      .replace(/^#### (.*)$/gm, '<h4>$1</h4>')
      .replace(/^### (.*)$/gm, '<h3>$1</h3>')
      .replace(/^## (.*)$/gm, '<h2>$1</h2>')
      .replace(/^# (.*)$/gm, '<h1>$1</h1>')
      // Unordered list: - item or * item
      .replace(/^- (.*)$/gm, '<li>$1</li>')
      .replace(/^\* (.*)$/gm, '<li>$1</li>')
      // Ordered list: 1. item
      .replace(/^\d+\. (.*)$/gm, '<li>$1</li>')
      // Blockquote: > text
      .replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>')
      // Horizontal rule: --- or ***
      .replace(/^---$/gm, '<hr>')
      .replace(/^\*\*\*$/gm, '<hr>')
      // Links: [text](url)
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
      // Images: ![alt](url)
      .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" />')
      // Convert newlines to paragraphs, but preserve other elements
      .replace(/^(?!<li>|<h[1-6]>|<blockquote>|<pre>|<hr>)(.*)$/gm, '<p>$1</p>')
      // Remove empty paragraphs
      .replace(/<p>\s*<\/p>/g, '')
      // Wrap consecutive unordered list items in <ul>
      .replace(/(<li>.*?<\/li>)+/g, match => {
        if (match.includes('<li>') && !match.includes('<ol>')) {
          return '<ul>' + match + '</ul>';
        }
        return match;
      })
      // Wrap consecutive ordered list items in <ol>
      .replace(/(<li>.*?<\/li>)+/g, match => {
        if (match.includes('<li>') && match.match(/^\d+\./)) {
          return '<ol>' + match + '</ol>';
        }
        return match;
      })
      // Wrap consecutive blockquote lines
      .replace(/(<blockquote>.*?<\/blockquote>)+/g, '<blockquote>$&</blockquote>');
    return html;
  };

  // Determine text size based on the setting
  const textSizeStyle = {
    fontSize: textSize === 'Small' ? '0.8em' : textSize === 'Large' ? '1.2em' : '1em'
  };

  // Determine theme color based on the setting
  const themeColorStyle = {
    color: themeColor === 'Green' ? '#00BFA5' : themeColor === 'Purple' ? '#9C27B0' : themeColor === 'Orange' ? '#FF9800' : '#3B82F6'
  };

  return (
    <div className="chat-window" style={textSizeStyle}>
      <div className="chat-header">
        <h2 style={themeColorStyle}>OmniChat-v1</h2>
        <div className="provider-model-info" style={themeColorStyle}>
          {provider && model ? `${provider} | ${model}` : 'No provider/model selected'}
        </div>
      </div>
      <div className="chat-messages">
        {messages.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#888' }}>No messages yet. Start chatting!</p>
        ) : (
          messages.map(message => (
            <div key={message.id} className={`message ${message.sender} ${message.isRetry ? 'retry-message' : ''} ${message.isRetryResponse ? 'retry-response' : ''}`}>
              <div className="message-content">
                {message.sender === 'ai' ? (
                  <div className="markdown-content">
                    <div dangerouslySetInnerHTML={{ __html: simpleMarkdownToHtml(message.text) }} />
                  </div>
                ) : (
                  <p>{message.text}</p>
                )}
                <span className="timestamp">{message.timestamp}</span>
              </div>
            </div>
          ))
        )}
      </div>
      <div className="chat-input">
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
          />
          <div className="input-icons">
            <button className="icon-button upload-icon" disabled={!input.trim()}>
              📤
            </button>
            <button className="icon-button send-icon" onClick={handleSendMessage} disabled={!input.trim()}>
              ✈️
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
