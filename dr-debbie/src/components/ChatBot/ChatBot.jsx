// src/components/ChatBot/ChatBot.jsx
import React, { useState, useEffect, useRef } from 'react';
import Canvas from './Canvas';
import { Mic, MicOff, Send, Volume2, VolumeX } from 'lucide-react';
import './ChatBot.css';

const ChatBot = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState(null);

  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        setMessage(transcript);
        
        if (event.results[current].isFinal) {
          handleSendMessage(transcript);
        }
      };

      recognition.onerror = (event) => {
        setError(`Speech recognition error: ${event.error}`);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    } else {
      setError('Speech recognition not supported in this browser');
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const handleSendMessage = async (text = message) => {
    try {
      const response = await fetch('/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: text }),
      });

      const data = await response.json();
      setResponse(data.response);
      speakResponse(data.response);
    } catch (error) {
      setError('Error communicating with server');
      console.error('Error:', error);
    }
  };

  const handleSpeechToText = () => {
    if (isListening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
  };

  const speakResponse = (text) => {
    if (!synthRef.current) return;

    // Cancel any ongoing speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = (event) => {
      setError(`Speech synthesis error: ${event.error}`);
      setIsSpeaking(false);
    };

    synthRef.current.speak(utterance);
  };

  const handleTextToSpeech = () => {
    if (isSpeaking) {
      synthRef.current.cancel();
      setIsSpeaking(false);
    } else if (response) {
      speakResponse(response);
    }
  };

  return (
    <div className="chatbot-panel">
      <div className="canvas-container">
        <Canvas />
      </div>
      {error && <div className="error-message">{error}</div>}
      <div className="chat-controls">
        <div className="mic-control">
          <button 
            onClick={handleSpeechToText} 
            className={`mic-button ${isListening ? 'active' : ''}`}
          >
            {isListening ? <MicOff /> : <Mic />}
          </button>
        </div>
        <div className="input-control">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your question here."
            className="chat-input"
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button onClick={() => handleSendMessage()} className="send-button">
            <Send />
          </button>
        </div>
        <div className="chat-response" id="chatResponse">
          {response}
        </div>
        <button 
          onClick={handleTextToSpeech} 
          className={`speak-button ${isSpeaking ? 'active' : ''}`}
        >
          {isSpeaking ? <VolumeX /> : <Volume2 />}
        </button>
      </div>
    </div>
  );
};

export default ChatBot;