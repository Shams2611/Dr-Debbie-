import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Google Gemini API Configuration
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Exercise configurations
    EXERCISES = {
        'squat': {
            'detector': 'SquatDetector',
            'description': 'Lower body exercise focusing on proper squat form'
        },
        'leg-raises': {
            'detector': 'LegRaiseDetector',
            'description': 'Lower body exercise for leg strength and stability'
        },
        'thoracic-extensions': {
            'detector': 'ThoracicExtensionDetector',
            'description': 'Upper back mobility exercise'
        },
        'shoulder-press': {
            'detector': 'ShoulderPressDetector',
            'description': 'Upper body strength exercise'
        },
        'shoulder-raise': {
            'detector': 'ShoulderRaiseDetector',
            'description': 'Shoulder mobility exercise'
        },
        'back-extension': {
            'detector': 'BackExtensionDetector',
            'description': 'Lower back mobility exercise'
        }
    }

    # Model configurations
    MODEL_CONFIG = {
        'pose_model_id': "yolov8n-pose.pt",
        'cerebras_model': "llama3.1-8b",
        'model_chunk_size': 1024/(2**4)
    }