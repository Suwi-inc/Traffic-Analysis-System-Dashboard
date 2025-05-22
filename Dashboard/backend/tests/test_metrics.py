from datetime import datetime, timedelta
from ..src.metrics import (
    calculate_lane_occupancy,
    vehicle_type_distribution,
    vehicle_counts_over_time,
)


def test_calculate_lane_occupancy():
    lane_occupancy_frames = {"lane_1": 70, "lane_2": 40, "lane_3": 0}
    total_frames = 100
    expected = {"lane_1": 70.0, "lane_2": 40.0, "lane_3": 0.0}
    result = calculate_lane_occupancy(lane_occupancy_frames, total_frames)
    assert result == expected


def test_calculate_lane_occupancy_zero_frames():
    lane_occupancy_frames = {"lane_1": 50}
    total_frames = 0
    expected = {"lane_1": 0.0}
    result = calculate_lane_occupancy(lane_occupancy_frames, total_frames)
    assert result == expected


def test_vehicle_type_distribution():
    vehicle_labels_per_lane = {
        "lane_1": ["car", "truck", "car", "bus"],
        "lane_2": ["motorbike", "car", "car"],
    }
    expected = {
        "lane_1": {"car": 2, "truck": 1, "bus": 1},
        "lane_2": {"motorbike": 1, "car": 2},
    }
    result = vehicle_type_distribution(vehicle_labels_per_lane)
    assert result == expected


def test_vehicle_counts_over_time_minute():
    base_time = datetime(2024, 1, 1, 14, 30)
    timestamps = {
        "lane_1": [
            base_time,
            base_time + timedelta(seconds=10),
            base_time + timedelta(minutes=1),
            base_time + timedelta(minutes=1),
        ]
    }
    expected = {"lane_1": {"2024-01-01 14:30": 2, "2024-01-01 14:31": 2}}
    result = vehicle_counts_over_time(timestamps, interval="minute")
    assert result == expected


def test_vehicle_counts_over_time_hour():
    base_time = datetime(2024, 1, 1, 10, 5)
    timestamps = {
        "lane_1": [
            base_time,
            base_time + timedelta(minutes=10),
            base_time + timedelta(hours=1),
            base_time + timedelta(hours=1, minutes=5),
        ]
    }
    expected = {"lane_1": {"2024-01-01 10": 2, "2024-01-01 11": 2}}
    result = vehicle_counts_over_time(timestamps, interval="hour")
    assert result == expected
