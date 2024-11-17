# app/detectors/back_extension_detector.py
from .base_detector import BaseDetector

class BackExtensionDetector(BaseDetector):
    def __init__(self, model):
        super().__init__(model)
        self.min_extension_angle = 170
        self.max_extension_angle = 190

    def check_form(self, keypoints):
        feedback = []
        highlights = []

        try:
            nose = np.array(keypoints['nose'][0])
            right_hip = np.array(keypoints['right-hip'][0])
            left_hip = np.array(keypoints['left-hip'][0])
            hips = (right_hip + left_hip) / 2

            right_knee = np.array(keypoints['right-knee'][0])
            left_knee = np.array(keypoints['left-knee'][0])
            knees = (right_knee + left_knee) / 2

        except KeyError as e:
            print(f"Missing keypoints: {e}")
            return "Keypoints not detected", []

        back_extension_angle = self.calculate_angle(nose, hips, knees)

        if back_extension_angle < self.min_extension_angle:
            feedback.append("Extend your back more.")
            highlights.append(('nose', 'right-hip', 'left-hip'))
        elif back_extension_angle > self.max_extension_angle:
            feedback.append("Reduce your extension, avoid hyperextending.")
            highlights.append(('nose', 'right-hip', 'left-hip'))
        else:
            feedback.append("Good back extension. Keep it gentle and controlled.")

        return " ".join(feedback), highlights

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