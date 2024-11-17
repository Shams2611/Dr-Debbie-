# app/detectors/__init__.py
from .base_detector import BaseDetector
from .squat_detector import SquatDetector
from .leg_raise_detector import LegRaiseDetector
from .back_extension_detector import BackExtensionDetector
from .shoulder_press_detector import ShoulderPressDetector
from .shoulder_raise_detector import ShoulderRaiseDetector
from .thoracic_extension_detector import ThoracicExtensionDetector

__all__ = [
    'BaseDetector',
    'SquatDetector',
    'LegRaiseDetector',
    'BackExtensionDetector',
    'ShoulderPressDetector',
    'ShoulderRaiseDetector',
    'ThoracicExtensionDetector'
]