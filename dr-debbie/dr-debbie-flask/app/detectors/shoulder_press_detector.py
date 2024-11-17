# app/detectors/shoulder_press_detector.py
from .base_detector import BaseDetector
import numpy as np

class ShoulderPressDetector(BaseDetector):
    def __init__(self, model):
        super().__init__(model)
        self.min_press_angle = 160
        self.max_flare_angle = 30

    def check_form(self, keypoints):
        feedback = []
        highlights = []

        try:
            right_shoulder = np.array(keypoints['right-shoulder'][0])
            left_shoulder = np.array(keypoints['left-shoulder'][0])
            
            right_elbow = np.array(keypoints['right-elbow'][0])
            left_elbow = np.array(keypoints['left-elbow'][0])
            
            right_hand = np.array(keypoints['right-hand'][0])
            left_hand = np.array(keypoints['left-hand'][0])
            
            right_hip = np.array(keypoints['right-hip'][0])
            left_hip = np.array(keypoints['left-hip'][0])
        except KeyError as e:
            print(f"Missing keypoints: {e}")
            return "Keypoints not detected", []

        right_press_angle = self.calculate_angle(right_hand, right_elbow, right_shoulder)
        left_press_angle = self.calculate_angle(left_hand, left_elbow, left_shoulder)

        right_flare_angle = self.calculate_angle(right_hip, right_shoulder, right_elbow)
        left_flare_angle = self.calculate_angle(left_hip, left_shoulder, left_elbow)

        if right_press_angle < self.min_press_angle:
            feedback.append("Extend your right arm fully.")
            highlights.append(('right-shoulder', 'right-elbow', 'right-hand'))
        if right_flare_angle > self.max_flare_angle:
            feedback.append("Keep your right arm straight, avoid flaring out.")
            highlights.append(('right-shoulder', 'right-elbow'))

        if left_press_angle < self.min_press_angle:
            feedback.append("Extend your left arm fully.")
            highlights.append(('left-shoulder', 'left-elbow', 'left-hand'))
        if left_flare_angle > self.max_flare_angle:
            feedback.append("Keep your left arm straight, avoid flaring out.")
            highlights.append(('left-shoulder', 'left-elbow'))

        if feedback:
            return " ".join(feedback), highlights
        else:
            return "Good form. Keep it up!", []

    def detect_per_frame(self, frame):
        frame, keypoints, results = self.get_keypoints(frame)

        if not keypoints:
            return frame

        try:
            feedback, highlights = self.check_form(keypoints)
            frame = self.add_feedback_text(frame, feedback)
            frame = self.draw_skeleton(frame, results, highlights, keypoints)
        except Exception as e:
            print(f"Error in form detection: {e}")

        return cv2.flip(frame, 1)