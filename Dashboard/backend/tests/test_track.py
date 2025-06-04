import numpy as np
from ..src.track import Tracker


def test_tracker_initialization():
    tracker = Tracker()
    assert tracker is not None


def test_tracker_tracking_empty_input():
    tracker = Tracker()
    frame = np.zeros((200, 200, 3), dtype=np.uint8)
    detections = []
    labels = []
    result = tracker.track(detections, frame, labels)
    assert isinstance(result, list)
