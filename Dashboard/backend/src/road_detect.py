import numpy as np
import cv2 as cv2


def fixColor(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def draw_lanes_on_frame(frame, lanes, color=(0, 255, 0), thickness=2, show_labels=True):
    """
    Draws polygonal lanes on the given frame.

    Parameters:
        frame (np.ndarray): The image/frame on which to draw.
        lanes (list): List of lane dicts with keys: 'points', 'label' (optional), and 'id'.
        color (tuple): BGR color of the lane polygon.
        thickness (int): Line thickness of the polygon edges.
        show_labels (bool): Whether to display labels near the lanes.

    Returns:
        np.ndarray: The modified frame with polygons drawn.
    """
    for lane in lanes:
        points = np.array(lane["points"], dtype=np.int32)
        cv2.polylines(frame, [points], isClosed=True, color=color, thickness=thickness)

        if show_labels:
            label = lane.get("label", lane["id"])
            # Use the first point to position the label
            text_position = tuple(points[0])
            cv2.putText(
                frame,
                label,
                text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

    return frame


def draw_lane_lines(img, left_line, right_line, color=[0, 0, 255], thickness=10):
    line_img = np.zeros_like(img)
    poly_pts = np.array(
        [
            [
                (left_line[0][0], left_line[0][1]),
                (left_line[0][2], left_line[0][3]),
                (right_line[0][2], right_line[0][3]),
                (right_line[0][0], right_line[0][1]),
            ]
        ],
        dtype=np.int32,
    )

    cv2.fillPoly(line_img, poly_pts, color)
    overlay = cv2.addWeighted(img, 1, line_img, 0.5, 0.0)
    return overlay


def get_overlay(res_right, res_left, imageres):

    for x in range(int(res_right.size / 4) - 1):
        imageres = draw_lane_lines(imageres, res_right[x], res_right[x + 1])

    for x in range(int(res_left.size / 4) - 1):
        imageres = draw_lane_lines(imageres, res_left[x], res_left[x + 1])

    imageres = draw_lane_lines(
        imageres,
        res_left[int(res_left.size / 4) - 1],
        res_right[int(res_right.size / 4) - 1],
        color=[255, 255, 255],
    )

    return imageres


def detect(image, h_threshold=80, distance_threshold=50):

    # We will convert the image to greyscale and run a Gaussian filter to remove small edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)

    # We will use Canny edge detection to create edges
    edges = cv2.Canny(
        gray, 70, 50
    )  # Important pareameters for accurate lines in various frame lighting conditions

    # Apply HoughLines

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=h_threshold,
        minLineLength=5,
        maxLineGap=250,
    )

    lines_with_x = [(line, (line[0][0] + line[0][2]) // 2) for line in lines]

    # Sort by x position (from left to right)
    lines_with_x.sort(key=lambda x: x[1])
    filtered_lines_x = []
    filtered_lines_y = []
    prev_x = None
    for line, x in lines_with_x:
        if (prev_x is None or abs(x - prev_x) >= distance_threshold) and (
            abs(line[0][1] - line[0][3]) > (abs(line[0][0] - line[0][2]) / 3)
        ):
            if line[0][1] > line[0][3]:
                filtered_lines_x.append(line)
                prev_x = x
            else:
                filtered_lines_y.append(line)
                prev_x = x

    res_right = np.array(filtered_lines_x, dtype=np.int32)
    res_left = np.array(filtered_lines_y, dtype=np.int32)

    return res_right, res_left
