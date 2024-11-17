// src/utils/speechUtils.js
export const initSpeechToText = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition is not supported in this browser');
      return null;
    }
  
    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
  
    return recognition;
  };
  
  export const initTextToSpeech = () => {
    if (!('speechSynthesis' in window)) {
      alert('Text to speech is not supported in this browser');
      return null;
    }
  
    return window.speechSynthesis;
  };
  
  export const speak = (text) => {
    const synthesis = window.speechSynthesis;
    if (!synthesis) return;
  
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
  
    synthesis.speak(utterance);
  };