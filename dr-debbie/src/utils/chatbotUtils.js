// src/utils/chatbotUtils.js
export const processMessage = async (message) => {
    // Replace this with your actual chatbot processing logic
    const responses = {
      hello: "Hi! How can I help you today?",
      help: "I can help you track your medications and guide you through physical therapy exercises.",
      default: "I'm here to help you with your health journey. Would you like to track medications or try some exercises?"
    };
  
    // Simple response logic - enhance this based on your needs
    const lowercaseMessage = message.toLowerCase();
    if (lowercaseMessage.includes('hello') || lowercaseMessage.includes('hi')) {
      return responses.hello;
    } else if (lowercaseMessage.includes('help')) {
      return responses.help;
    }
    return responses.default;
  };
  
  export const formatResponse = (response) => {
    return {
      text: response,
      timestamp: new Date().toISOString(),
      type: 'bot'
    };
  };
  
  export const validateMessage = (message) => {
    return message.trim().length > 0;
  };
  
  export const handleError = (error) => {
    console.error('Chatbot Error:', error);
    return {
      text: "I'm having trouble processing your request. Please try again.",
      timestamp: new Date().toISOString(),
      type: 'error'
    };
  };