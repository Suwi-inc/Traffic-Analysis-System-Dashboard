import cv2
from ..src.track import Tracker


def test_tracker_initialization():
    tracker = Tracker()
    assert tracker is not None


def test_tracker_tracking_empty_input():
    tracker = Tracker()
    frame = cv2.imread("./assets/test_image.jpg")
    detections = []
    labels = []
    result = tracker.track(detections, frame, labels)
    assert isinstance(result, list)
