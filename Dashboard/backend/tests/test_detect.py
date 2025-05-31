import cv2
import numpy as np
from ..src.detect import YoloDetector


def test_yolo_detector_initialization():
    detector = YoloDetector(
        model_path="./assets/yolo11m.pt", confidence=0.1, device="cpu"
    )
    assert detector is not None


def test_yolo_detection_output_format():
    detector = YoloDetector(
        model_path="./assets/yolo11m.pt", confidence=0.1, device="cpu"
    )
    test_image = np.zeros((200, 200, 3), dtype=np.uint8)
    detections, labels = detector.detect(test_image, "cpu")
    assert isinstance(detections, list)
    assert isinstance(labels, list)
