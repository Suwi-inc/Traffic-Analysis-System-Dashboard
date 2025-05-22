import numpy as np
import cv2
from ..src.road_detect import (
    fixColor,
    draw_lanes_on_frame,
    draw_lane_lines,
    get_overlay,
    detect,
)


def test_fix_color():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    rgb_image = fixColor(image)
    assert rgb_image.shape == image.shape
    assert (rgb_image[:, :, 0] == 0).all()


def test_draw_lanes_on_frame():
    frame = np.zeros((200, 200, 3), dtype=np.uint8)
    lanes = [
        {
            "id": "1",
            "points": [[10, 10], [50, 10], [50, 50], [10, 50]],
            "label": "Lane 1",
        },
        {"id": "2", "points": [[60, 10], [100, 10], [100, 50], [60, 50]]},
    ]
    output = draw_lanes_on_frame(frame.copy(), lanes)
    assert output.shape == frame.shape
    assert (output != frame).any()


def test_draw_lane_lines():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    left_line = np.array([[10, 10, 10, 90]])
    right_line = np.array([[90, 10, 90, 90]])
    output = draw_lane_lines(img.copy(), left_line, right_line)
    assert output.shape == img.shape
    assert (output != img).any()


def test_get_overlay():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    left = np.array([[[10, 90, 10, 10]], [[10, 10, 30, 10]]])
    right = np.array([[[90, 90, 90, 10]], [[90, 10, 70, 10]]])
    overlay = get_overlay(right, left, img.copy())
    assert overlay.shape == img.shape
    assert (overlay != img).any()


def test_detect_lines():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.line(img, (20, 0), (20, 99), (255, 255, 255), 2)
    cv2.line(img, (80, 0), (80, 99), (255, 255, 255), 2)
    right, left = detect(img)

    assert isinstance(right, np.ndarray)
    assert isinstance(left, np.ndarray)
