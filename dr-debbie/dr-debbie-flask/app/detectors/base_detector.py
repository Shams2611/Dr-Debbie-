# app/detectors/base_detector.py
import cv2
import numpy as np
import supervision as sv
from abc import ABC, abstractmethod

class BaseDetector(ABC):
    def __init__(self, model):
        self.model = model

    def calculate_angle(self, a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)

    def get_keypoints(self, frame):
        frame = cv2.flip(frame, 1)
        results = self.model.infer(frame)[0]

        keypoints = {}
        for i in results.predictions:
            for j in i.keypoints:
                keypoints[j.class_name.lower().replace(' ', '-')] = [(int(j.x), int(j.y))]
                cv2.circle(frame, (int(j.x), int(j.y)), radius=10, color=(0, 0, 255), thickness=-1)

        return frame, keypoints, results

    def draw_skeleton(self, frame, results, highlights=None, keypoints=None):
        annotated_image = sv.EdgeAnnotator(color=sv.Color.GREEN, thickness=5).annotate(
            frame, sv.KeyPoints.from_inference(results)
        )

        if highlights and keypoints:
            try:
                for joint_pair in highlights:
                    for i in range(len(joint_pair) - 1):
                        start_point = keypoints[joint_pair[i]][0]
                        end_point = keypoints[joint_pair[i+1]][0]
                        cv2.line(annotated_image, start_point, end_point, (0, 0, 255), 5)
            except Exception as e:
                print(f"Error in drawing highlights: {e}")

        return annotated_image

    def add_feedback_text(self, frame, feedback):
        cv2.putText(
            frame, 
            feedback, 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (0, 255, 0), 
            2
        )
        return frame

    @abstractmethod
    def check_form(self, keypoints):
        pass

    @abstractmethod
    def detect_per_frame(self, frame):
        pass