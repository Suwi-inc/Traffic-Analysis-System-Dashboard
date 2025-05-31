from datetime import datetime
import os
import time
import cv2
import json
import base64
import asyncio
import numpy as np
from collections import defaultdict
from .db.db_model import SessionLocal
from .db.store_metrics import store_metrics_data

from .detect import YoloDetector
from .track import Tracker
from .road_detect import draw_lanes_on_frame
from .metrics import (
    calculate_lane_occupancy,
    vehicle_counts_over_time,
    vehicle_type_distribution,
)

MODEL_PATH = "./models/yolo11m.pt"
PREDEFINED_LANES = "predefined_lanes.json"


def load_lane_polygons(base_dir):
    lanes_path = os.path.join(base_dir, PREDEFINED_LANES)
    with open(lanes_path) as f:
        data = json.load(f)
    lane_polygons = {
        lane["id"]: np.array(lane["points"], dtype=np.int32) for lane in data["lanes"]
    }
    return data["lanes"], lane_polygons


def draw_vehicle_annotations(frame, tracking_data):
    for tracking_id, bbox, label in tracking_data:
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (181, 255, 135), 1)
        cv2.putText(
            frame,
            f"{label} {int(tracking_id)}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (181, 255, 135),
            1,
        )
    return frame


def update_lane_metrics(
    tracking_data,
    lane_polygons,
    entries,
    counts,
    labels_per_lane,
    occupancy,
    vehicle_timestamps,
):
    occupied_lanes = set()
    for tracking_id, bbox, label in tracking_data:
        x1, y1, x2, y2 = map(int, bbox)
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        for lane_id, polygon in lane_polygons.items():
            if cv2.pointPolygonTest(polygon, center, False) >= 0:
                if tracking_id not in entries[lane_id]:
                    vehicle_timestamps[lane_id].append(datetime.now())
                    entries[lane_id].add(tracking_id)
                    counts[lane_id] += 1
                    labels_per_lane[lane_id].append(label)
                occupied_lanes.add(lane_id)
                break
    for lane_id in occupied_lanes:
        occupancy[lane_id] += 1


def draw_lane_counters(frame, lanes, vehicle_counts):
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
    return frame


async def stream_frame(websocket, payload):
    _, buffer = cv2.imencode(".jpg", payload["frame"])
    jpg_as_text = base64.b64encode(buffer).decode("utf-8")
    payload["frame"] = jpg_as_text
    await websocket.send_text(json.dumps(payload))


async def process_and_stream_analysis(
    websocket, video_path, vehicles=True, counter=True, show_lanes=False
):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not video_path or not os.path.exists(video_path):
        await websocket.send_text(json.dumps({"error": "No video found"}))
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        await websocket.send_text(json.dumps({"error": "Could not open video"}))
        return

    lanes, lane_polygons = load_lane_polygons(base_dir)
    detector = YoloDetector(model_path=MODEL_PATH, confidence=0.1)
    tracker = Tracker()

    vehicle_entries = {lane_id: set() for lane_id in lane_polygons.keys()}
    vehicle_counts = {lane_id: 0 for lane_id in lane_polygons.keys()}
    vehicle_labels_per_lane = {lane_id: [] for lane_id in lane_polygons.keys()}
    vehicle_timestamps = {lane_id: [] for lane_id in lane_polygons.keys()}
    lane_occupancy_frames = defaultdict(int)
    total_frames = 0
    final_metrics = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        start_time = time.perf_counter()
        detections, labels = detector.detect(frame)
        tracking_data = tracker.track(detections, frame, labels)

        update_lane_metrics(
            tracking_data,
            lane_polygons,
            vehicle_entries,
            vehicle_counts,
            vehicle_labels_per_lane,
            lane_occupancy_frames,
            vehicle_timestamps,
        )

        if vehicles:
            frame = draw_vehicle_annotations(frame, tracking_data)
        if show_lanes:
            frame = draw_lanes_on_frame(frame, lanes)
        if counter:
            frame = draw_lane_counters(frame, lanes, vehicle_counts)

        type_distribution = vehicle_type_distribution(vehicle_labels_per_lane)
        occupancy = calculate_lane_occupancy(lane_occupancy_frames, total_frames)
        counts_per_minute = vehicle_counts_over_time(
            vehicle_timestamps, interval="minute"
        )
        counts_per_hour = vehicle_counts_over_time(vehicle_timestamps, interval="hour")
        end_time = time.perf_counter()
        fps = 1 / (end_time - start_time)

        final_metrics = payload = {
            "frame": frame,
            "type_distribution": type_distribution,
            "occupancy": occupancy,
            "counts_per_minute": counts_per_minute,
            "counts_per_hour": counts_per_hour,
            "fps": fps,
        }

        await stream_frame(websocket, payload)
        await asyncio.sleep(0.017)

    if final_metrics:
        with SessionLocal() as db:
            store_metrics_data(
                db,
                video_name=os.path.basename(video_path),
                type_distribution=final_metrics["type_distribution"],
                occupancy=final_metrics["occupancy"],
            )
    await websocket.close()
    cap.release()
