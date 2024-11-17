# app/detectors/shoulder_raise_detector.py
from .base_detector import BaseDetector
import numpy as np

class ShoulderRaiseDetector(BaseDetector):
    def __init__(self, model):
        super().__init__(model)
        self.min_raise_angle = 70
        self.max_raise_angle = 110

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

        right_raise_angle = self.calculate_angle(right_hip, right_shoulder, right_elbow)
        left_raise_angle = self.calculate_angle(left_hip, left_shoulder, left_elbow)

        if right_raise_angle < self.min_raise_angle:
            feedback.append("Raise your right arm higher.")
            highlights.append(('right-shoulder', 'right-elbow', 'right-hand'))
        elif right_raise_angle > self.max_raise_angle:
            feedback.append("Lower your right arm, avoid over-raising.")
            highlights.append(('right-shoulder', 'right-elbow', 'right-hand'))

        if left_raise_angle < self.min_raise_angle:
            feedback.append("Raise your left arm higher.")
            highlights.append(('left-shoulder', 'left-elbow', 'left-hand'))
        elif left_raise_angle > self.max_raise_angle:
            feedback.append("Lower your left arm, avoid over-raising.")
            highlights.append(('left-shoulder', 'left-elbow', 'left-hand'))

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