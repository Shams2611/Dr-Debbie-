# app/models/cerebras_model.py
class CerebrasModel:
    def __init__(self, model_name="llama3.1-8b", chunk_size=64):
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.context = ""

    def getResponse(self, input_text):
        """
        Get response from the Cerebras model
        Args:
            input_text (str): Input text to process
        Returns:
            str: Generated response
        """
        try:
            # Add input to context
            self.context += f"\nHuman: {input_text}\nAssistant: "
            
            # Here you would typically make a call to your actual model
            # This is a placeholder response
            response = "I understand you want assistance with physical therapy. I'll guide you through the exercises safely and effectively."
            
            # Add response to context
            self.context += response
            
            return response
        except Exception as e:
            print(f"Error in model response: {e}")
            return "I apologize, but I'm having trouble processing your request. Please try again."

    def reset_context(self):
        """Reset the conversation context"""
        self.context = ""