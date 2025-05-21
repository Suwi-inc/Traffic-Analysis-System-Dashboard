import cv2
import time
import json
import argparse
from Dashboard.backend.src.detect import YoloDetector
from Dashboard.backend.src.track import Tracker
from datetime import datetime
from collections import defaultdict
from road_detect import get_overlay, detect, fixColor, draw_lanes_on_frame
from metrics import calculate_lane_occupancy, vehicle_type_distribution

import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Vehicle Detection and Tracking")
parser.add_argument(
    "--lanes",
    type=str,
    choices=["yes", "no"],
    default="yes",
    help="Show lanes in the video (yes/no)",
)
parser.add_argument(
    "--vehicles",
    type=str,
    choices=["yes", "no"],
    default="yes",
    help="Show vehicle bounding boxes in the video (yes/no)",
)
parser.add_argument(
    "--counter",
    type=str,
    choices=["yes", "no"],
    default="yes",
    help="Show vehicle counters in the video (yes/no)",
)
parser.add_argument(
    "--predefined_lanes",
    type=str,
    choices=["yes", "no"],
    default="yes",
    help="Use user defined lane coordinates for the regions of interests (yes/no)",  # User defined lanes are stored in ./predefined_lanes.json
)
args = parser.parse_args()

MODEL_PATH = "../models/yolo11m.pt"
VIDEO_PATH = "../assets/cars2.mp4"
OUTPUT_VIDEO_PATH = (
    f"./outputs/video/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}output.mp4"
)

lanes = []
lane_polygons = {}  # dict of all lane coordinates
current_label = 1


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    if args.predefined_lanes == "yes":
        with open("predefined_lanes.json") as f:
            data = json.load(f)
        lanes = data["lanes"]
        for lane in lanes:
            lane_id = lane["id"]
            points = lane["points"]
            polygon = np.array(points, dtype=np.int32)
            lane_polygons[lane_id] = polygon

    else:
        ret, first_frame = cap.read()
        if not ret:
            print("Error: Could not read the first frame.")
            return
        right_lane, left_lane = detect(first_frame)

        if right_lane.any() and left_lane.any():
            with open("lane_coordinates.json", "w") as f:
                json.dump(
                    {
                        "right_lane": right_lane.tolist(),
                        "left_lane": left_lane.tolist(),
                    },
                    f,
                )
        else:
            print("No lanes were detected.")
            return

    detector = YoloDetector(model_path=MODEL_PATH, confidence=0.1)
    tracker = Tracker()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (frame_width, frame_height))

    points = []

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

        start_time = time.perf_counter()
        detections, labels = detector.detect(frame)
        tracking_data = tracker.track(detections, frame, labels)

        for tracking_id, bounding_box, label in tracking_data:
            x1, y1, x2, y2 = (
                int(bounding_box[0]),
                int(bounding_box[1]),
                int(bounding_box[2]),
                int(bounding_box[3]),
            )
            points.append((x1, y1, x2, y2))

            if args.vehicles == "yes":
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

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # counting
            for lane_id, polygon in lane_polygons.items():
                result = cv2.pointPolygonTest(polygon, (center_x, center_y), False)

                if result >= 0:  # Vehicle is inside the lane
                    if tracking_id not in vehicle_entries[lane_id]:
                        vehicle_entries[lane_id].add(tracking_id)  # Mark as counted
                        vehicle_counts[lane_id] += 1
                        vehicle_labels_per_lane[lane_id].append(label)
                    lane_occupied_this_frame.add(lane_id)
                    break
        for lane_id in lane_occupied_this_frame:
            lane_occupancy_frames[lane_id] += 1
        if args.lanes == "yes":
            frame = draw_lanes_on_frame(frame, lanes)
        # Display the vehicle counts on the frame if --counter=yes
        if args.counter == "yes":
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

        out.write(frame)

        end_time = time.perf_counter()
        fps = 1 / (end_time - start_time)
        print(f"Current fps: {fps}")

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

    type_distribution = vehicle_type_distribution(vehicle_labels_per_lane)
    occupancy = calculate_lane_occupancy(lane_occupancy_frames, total_frames)

    metrics_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lane_occupancy": occupancy,
        "vehicle_type_distribution": type_distribution,
    }
    with open("./outputs/metrics/metrics_data.json", "a") as f:
        json.dump(metrics_data, f, indent=4)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Output video saved to: {OUTPUT_VIDEO_PATH}")


if __name__ == "__main__":
    main()
