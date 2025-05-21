import os
import cv2
import json
import base64
import asyncio
from collections import defaultdict
from datetime import datetime
import numpy as np
from .detect import YoloDetector
from .track import Tracker
from .road_detect import detect, draw_lanes_on_frame
from .metrics import calculate_lane_occupancy, vehicle_type_distribution

# To do add parameters to show certain data in the video

MODEL_PATH = "./models/yolo11m.pt"
PREDEFINED_LANES = "predefined_lanes.json"

lanes = []
lane_polygons = {}


async def process_and_stream_analysis(
    websocket, VIDEO_PATH: str, vehicles=True, counter=True, show_lanes=False
):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if not VIDEO_PATH or not os.path.exists(VIDEO_PATH):
        await websocket.send_text(json.dumps({"error": "No uploaded video found."}))
        return

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Load predefined lanes
    lanes_path = os.path.join(BASE_DIR, ".", PREDEFINED_LANES)
    with open(lanes_path) as f:
        data = json.load(f)
    global lanes
    lanes = data["lanes"]
    for lane in lanes:
        lane_id = lane["id"]
        points = lane["points"]
        polygon = np.array(points, dtype=np.int32)
        lane_polygons[lane_id] = polygon

    detector = YoloDetector(model_path=MODEL_PATH, confidence=0.1)
    tracker = Tracker()

    vehicle_entries = {lane_id: set() for lane_id in lane_polygons.keys()}
    vehicle_counts = {lane_id: 0 for lane_id in lane_polygons.keys()}
    vehicle_labels_per_lane = {lane_id: [] for lane_id in lane_polygons.keys()}
    lane_occupancy_frames = defaultdict(int)
    total_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        lane_occupied_this_frame = set()

        detections, labels = detector.detect(frame)
        tracking_data = tracker.track(detections, frame, labels)

        for tracking_id, bounding_box, label in tracking_data:
            x1, y1, x2, y2 = map(int, bounding_box)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            if vehicles:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (181, 255, 135), 1)
                cv2.putText(
                    frame,
                    f"{str(label)} {int(tracking_id)}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (181, 255, 135),
                    1,
                )
            for lane_id, polygon in lane_polygons.items():
                result = cv2.pointPolygonTest(polygon, (center_x, center_y), False)
                if result >= 0:
                    if tracking_id not in vehicle_entries[lane_id]:
                        vehicle_entries[lane_id].add(tracking_id)
                        vehicle_counts[lane_id] += 1
                        vehicle_labels_per_lane[lane_id].append(label)
                    lane_occupied_this_frame.add(lane_id)
                    break

        for lane_id in lane_occupied_this_frame:
            lane_occupancy_frames[lane_id] += 1

        if show_lanes:
            frame = draw_lanes_on_frame(frame, lanes)
        if counter:
            y_offset = 30
            for lane in lanes:
                lane_id = lane["id"]
                label = lane.get("label", lane_id)
                direction = lane.get("direction", "Undefined")
                count = vehicle_counts.get(lane_id, 0)
                cv2.putText(
                    frame,
                    f"{label} ({direction}): {count}",
                    (10, y_offset),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (50, 255, 0),
                    1,
                )
                y_offset += 30

        _, buffer = cv2.imencode(".jpg", frame)
        jpg_as_text = base64.b64encode(buffer).decode("utf-8")
        await websocket.send_text(json.dumps({"frame": jpg_as_text}))

        await asyncio.sleep(0.033)  # ~30fps

    cap.release()
