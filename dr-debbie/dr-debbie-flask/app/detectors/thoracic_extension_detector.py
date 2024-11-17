# app/detectors/thoracic_extension_detector.py
from .base_detector import BaseDetector
import numpy as np

class ThoracicExtensionDetector(BaseDetector):
    def __init__(self, model):
        super().__init__(model)
        self.min_extension_angle = 10
        self.max_extension_angle = 30

    def check_form(self, keypoints):
        feedback = []
        highlights = []

        try:
            right_hip = np.array(keypoints['right-hip'][0])
            left_hip = np.array(keypoints['left-hip'][0])
            pelvis_center = (right_hip + left_hip) / 2
            
            right_shoulder = np.array(keypoints['right-shoulder'][0])
            left_shoulder = np.array(keypoints['left-shoulder'][0])
            upper_back_center = (right_shoulder + left_shoulder) / 2

            nose = np.array(keypoints['nose'][0])
        except KeyError as e:
            print(f"Missing keypoints: {e}")
            return "Keypoints not detected", []

        thoracic_extension_angle = self.calculate_angle(nose, upper_back_center, pelvis_center)

        if thoracic_extension_angle < self.min_extension_angle:
            feedback.append("Extend your upper back more.")
            highlights.append(('right-shoulder', 'left-shoulder'))
        elif thoracic_extension_angle > self.max_extension_angle:
            feedback.append("Extend less, avoid overextending your lower back.")
            highlights.append(('right-shoulder', 'left-shoulder'))
        else:
            feedback.append("Good thoracic extension, keep the movement controlled.")

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