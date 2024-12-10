from flask import Blueprint, request, jsonify
import google.generativeai as genai
import base64
import os
from PIL import Image
import io
import logging

prescription_bp = Blueprint('prescription', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
try:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("Google API key not found in environment variables")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise

@prescription_bp.route('/api/analyze-prescription', methods=['POST'])
def analyze_prescription():
    """
    Endpoint to analyze prescription images using Google's Gemini API.
    Expects a base64 encoded image in the request body.
    """
    try:
        # Get base64 image from request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400

        # Convert base64 to image
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            logger.error(f"Failed to process image: {str(e)}")
            return jsonify({'error': 'Invalid image format'}), 400

        # Analyze with Gemini
        prompt = """
        Analyze this prescription image and extract the following information.
        For each medication, provide:
        - Name of the medication
        - Dosage
        - Timing (specify if Morning, Day, or Night)
        - Any special instructions

        Format each medication as:
        Medication X:
        Name: [medication name]
        Dosage: [dosage]
        Timing: [timing]
        Instructions: [instructions]
        """

        try:
            response = model.generate_content([prompt, image])
            if not response or not response.text:
                raise ValueError("Empty response from Gemini API")
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return jsonify({'error': 'Failed to analyze prescription'}), 500

        # Process Gemini's response
        try:
            medications = parse_gemini_response(response.text)
            if not medications:
                return jsonify({'error': 'No medications found in the prescription'}), 400
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {str(e)}")
            return jsonify({'error': 'Failed to process prescription data'}), 500

        return jsonify({
            'success': True,
            'medications': medications
        })

    except Exception as e:
        logger.error(f"Unexpected error in analyze_prescription: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

def parse_gemini_response(response_text):
    """
    Parse Gemini's response text into the application's medication format.
    Returns list of medications with name, days array, and time.
    """
    medications = []
    current_med = None
    
    try:
        # Split response into lines and process
        lines = response_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Start new medication entry
            if 'medication' in line.lower() or 'name:' in line.lower():
                if current_med and current_med['name']:  # Only add if it has a name
                    medications.append(current_med)
                current_med = {
                    'name': '',
                    'days': [True] * 7,  # Default to every day
                    'time': 'Morning',   # Default timing
                }
                
            if current_med:
                # Extract medication name
                if 'name:' in line.lower():
                    current_med['name'] = line.split('name:')[1].strip()
                    
                # Process timing information
                elif 'timing:' in line.lower() or 'frequency:' in line.lower():
                    timing_info = line.lower()
                    if 'night' in timing_info:
                        current_med['time'] = 'Night'
                    elif 'afternoon' in timing_info or 'evening' in timing_info:
                        current_med['time'] = 'Day'
                    
                    # Parse specific days if mentioned
                    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                    if any(day in timing_info for day in days):
                        current_med['days'] = [day in timing_info for day in days]
                    
                # Add dosage to name
                elif 'dosage:' in line.lower():
                    dosage = line.split('dosage:')[1].strip()
                    if current_med['name']:
                        current_med['name'] = f"{current_med['name']} ({dosage})"
                    
                # Add instructions to name
                elif 'instruction' in line.lower():
                    instructions = line.split(':')[1].strip()
                    if current_med['name']:
                        current_med['name'] = f"{current_med['name']} - {instructions}"
                        
        # Add the last medication if exists and has a name
        if current_med and current_med['name']:
            medications.append(current_med)
            
    except Exception as e:
        logger.error(f"Error parsing Gemini response: {str(e)}")
        raise

    return medications

# Utility function to validate image
def is_valid_image(image_data):
    """
    Validate if the provided data is a valid image.
    """
    try:
        Image.open(io.BytesIO(base64.b64decode(image_data)))
        return True
    except Exception:
        return False

# Example usage and test
if __name__ == "__main__":
    # Test the parser with sample data
    sample_response = """
    Medication 1:
    Name: Amoxicillin
    Dosage: 500mg
    Timing: Morning and Night
    Instructions: Take with food

    Medication 2:
    Name: Ibuprofen
    Dosage: 400mg
    Timing: Every 8 hours
    Instructions: Take after meals
    """
    
    try:
        result = parse_gemini_response(sample_response)
        print("Parsed medications:", result)
    except Exception as e:
        print(f"Error testing parser: {str(e)}")