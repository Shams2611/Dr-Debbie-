# app/detectors/squat_detector.py
from .base_detector import BaseDetector
import numpy as np

class SquatDetector(BaseDetector):
    def __init__(self, model):
        super().__init__(model)
        self.correct_squat_angle_min = 150
        self.correct_squat_angle_max = 180
        self.max_incorrect_reps = 5
        self.incorrect_movement_count = 0

    def check_form(self, keypoints):
        feedback = []
        highlights = []

        try:
            right_hip = np.array(keypoints['right-hip'][0])
            right_knee = np.array(keypoints['right-knee'][0])
            right_foot = np.array(keypoints['right-foot'][0])

            left_hip = np.array(keypoints['left-hip'][0])
            left_knee = np.array(keypoints['left-knee'][0])
            left_foot = np.array(keypoints['left-foot'][0])
        except KeyError as e:
            print(f"Missing keypoints: {e}")
            return "Keypoints not detected", []

        right_leg_angle = self.calculate_angle(right_hip, right_knee, right_foot)
        left_leg_angle = self.calculate_angle(left_hip, left_knee, left_foot)

        if right_leg_angle < self.correct_squat_angle_min:
            feedback.append("Raise your body, your right leg is squatting too low.")
            highlights.append(('right-hip', 'right-knee', 'right-foot'))
        elif right_leg_angle > self.correct_squat_angle_max:
            feedback.append("Lower your body, your right leg is not bent enough.")
            highlights.append(('right-hip', 'right-knee', 'right-foot'))

        if left_leg_angle < self.correct_squat_angle_min:
            feedback.append("Raise your body, your left leg is squatting too low.")
            highlights.append(('left-hip', 'left-knee', 'left-foot'))
        elif left_leg_angle > self.correct_squat_angle_max:
            feedback.append("Lower your body, your left leg is not bent enough.")
            highlights.append(('left-hip', 'left-knee', 'left-foot'))

        if feedback:
            self.incorrect_movement_count += 1
            if self.incorrect_movement_count >= self.max_incorrect_reps:
                return "Adjust your form. " + " ".join(feedback), highlights
        else:
            self.incorrect_movement_count = 0
            return "Good form. Keep it up!", []

        return "Continue the exercise", []

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