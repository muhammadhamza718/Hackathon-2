import React, { useState, useEffect, useRef } from 'react';
import TodoList from './TodoList'; // Import the new TodoList component
import './TodoChat.css'; // We'll create this CSS file separately

const TodoChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Function to scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend API - using environment variable or default
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Parse the response to check if it contains todo data
      let messageContent = data.response || 'Sorry, I could not process your request.';
      let hasTodos = false;
      let todos = [];

      // Try to parse the response to see if it contains todo data
      try {
        // Attempt to parse the response as JSON to see if it contains todo data
        const parsedResponse = JSON.parse(data.response);
        if (parsedResponse.success && parsedResponse.todos && Array.isArray(parsedResponse.todos)) {
          hasTodos = true;
          todos = parsedResponse.todos;
          messageContent = parsedResponse.message || 'Here are your todos:';
        }
      } catch (e) {
        // If parsing fails, use the response as plain text
        messageContent = data.response || 'Sorry, I could not process your request.';
      }

      // Add bot response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: messageContent,
        sender: 'bot',
        timestamp: new Date().toISOString(),
        hasTodos: hasTodos,
        todos: todos
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="todo-chat-container">
      <div className="chat-header">
        <h2>Todo Chat Assistant</h2>
        <p>Ask me to add, list, complete, or manage your todos</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your Todo Assistant. How can I help you today?</p>
            <div className="suggestions">
              <button
                onClick={() => setInputValue('Add a new todo: Buy groceries')}
                className="suggestion-btn"
              >
                Add a new todo: Buy groceries
              </button>
              <button
                onClick={() => setInputValue('List all my todos')}
                className="suggestion-btn"
              >
                List all my todos
              </button>
              <button
                onClick={() => setInputValue('Mark todo #1 as completed')}
                className="suggestion-btn"
              >
                Mark todo #1 as completed
              </button>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
            >
              <div className="message-content">
                {message.text}
                {message.hasTodos && message.todos && message.todos.length > 0 && (
                  <div className="todo-list-response">
                    <TodoList todos={message.todos} showHeader={false} />
                  </div>
                )}
              </div>
              <div className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot loading">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here... (e.g., 'Add a todo: Buy milk')"
          className="chat-input"
          rows="3"
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default TodoChat;