from flask import Flask
from config import Config
from .models.cerebras_model import CerebrasModel
from ultralytics import YOLO  # Changed from inference import

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize models - changed to use YOLO directly
    app.model = YOLO(app.config['MODEL_CONFIG']['pose_model_id'])
    app.cerebras_model = CerebrasModel(
        model_name=app.config['MODEL_CONFIG']['cerebras_model'],
        chunk_size=app.config['MODEL_CONFIG']['model_chunk_size']
    )
    
    # Initialize last_frame for video processing
    app.last_frame = None

    # Register blueprints
    from .routes import bp as main_bp
    from .routes.prescription import prescription_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(prescription_bp)

    # Ensure upload directory exists
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app