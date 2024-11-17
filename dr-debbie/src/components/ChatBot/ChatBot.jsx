// src/components/ChatBot/ChatBot.jsx
import React, { useState, useEffect } from 'react';
import Canvas from './Canvas';
import { initSpeechToText, initTextToSpeech } from "../../utils/speechUtils";
import './ChatBot.css';

const ChatBot = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSendMessage = () => {
    // Implement chatbot logic here
    console.log('Sending message:', message);
  };

  const handleSpeechToText = () => {
    // Implement speech to text logic
  };

  const handleTextToSpeech = () => {
    // Implement text to speech logic
  };

  return (
    <div className="chatbot-panel">
      <div className="canvas-container">
        <Canvas />
      </div>
      <div className="chat-controls">
        <div className="mic-control">
          <button onClick={handleSpeechToText} className="mic-button">
            Mic
          </button>
        </div>
        <div className="input-control">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your question here."
            className="chat-input"
          />
          <button onClick={handleSendMessage} className="send-button">
            Send
          </button>
        </div>
        <div className="chat-response" id="chatResponse">
          {response}
        </div>
        <button onClick={handleTextToSpeech} className="speak-button">
          Speak
        </button>
      </div>
    </div>
  );
};

export default ChatBot;