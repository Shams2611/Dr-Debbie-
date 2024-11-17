# app/routes.py
from flask import Blueprint, render_template, Response, request, redirect, jsonify, current_app
import cv2
import numpy as np
from .detectors import (
    SquatDetector,
    LegRaiseDetector,
    BackExtensionDetector,
    ShoulderPressDetector,
    ShoulderRaiseDetector,
    ThoracicExtensionDetector
)
import os

bp = Blueprint('main', __name__)

# Create detector mapping
DETECTOR_MAP = {
    'squat': SquatDetector,
    'leg-raises': LegRaiseDetector,
    'thoracic-extensions': ThoracicExtensionDetector,
    'shoulder-press': ShoulderPressDetector,
    'shoulder-raise': ShoulderRaiseDetector,
    'back-extension': BackExtensionDetector
}

@bp.route('/')
def home():
    return redirect('/home')

@bp.route('/home')
def index():
    return render_template('index.html')

@bp.route('/prompt', methods=['POST'])
def respond():
    try:
        data = request.get_json()
        inp = data["input"]
        res = current_app.cerebras_model.getResponse(inp)
        return jsonify({'response': res, 'inp': inp})
    except Exception as e:
        print("Error caught:", e)
        return jsonify({"message": "failed to parse input"}), 400

@bp.route('/get_user_info', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        sex = data.get('sex')
        
        if not all([name, age, sex]):
            return jsonify({"message": "Missing required fields"}), 400
            
        inp = f"Hi. My name is {name}. I am {age} years of age and my gender is {sex}."
        res = current_app.cerebras_model.getResponse(inp)
        return jsonify({'response': res, 'inp': inp})
    except Exception as e:
        print("Error caught:", e)
        return jsonify({"message": "Server error"}), 500

@bp.route("/video/<exercise>")
def video(exercise):
    if exercise not in DETECTOR_MAP:
        return "Invalid exercise type", 400
    return render_template('video.html', exercise=exercise)

@bp.route('/video_feed/<exercise>')
def video_feed(exercise):
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(exercise),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/video_stream', methods=['POST'])
def video_stream():
    if 'image' not in request.files:
        return "No image part", 400
    
    img_bytes = request.files['image'].read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is not None:
        current_app.last_frame = img
        return "Frame received", 200
    return "Failed to decode image", 400

def gen_frames(exercise):
    detector_class = DETECTOR_MAP.get(exercise, BackExtensionDetector)
    detector = detector_class(current_app.model)
    
    while True:
        frame = current_app.last_frame
        if frame is not None:
            try:
                frame = detector.detect_per_frame(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(f"Error in frame generation: {e}")
                continue