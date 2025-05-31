from datetime import datetime
import pytest
import numpy as np
import json
from unittest import mock
from collections import defaultdict
from ..src.process_and_stream_analysis import (
    load_lane_polygons,
    draw_vehicle_annotations,
    update_lane_metrics,
    draw_lane_counters,
    stream_frame,
)


@pytest.fixture
def mock_lanes_file(tmp_path):
    data = {
        "lanes": [
            {"id": "1", "points": [[0, 0], [100, 0], [100, 100], [0, 100]]},
            {"id": "2", "points": [[110, 0], [210, 0], [210, 100], [110, 100]]},
        ]
    }
    file_path = tmp_path / "predefined_lanes.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return str(tmp_path)


def test_load_lane_polygons(mock_lanes_file):
    from ..src.process_and_stream_analysis import PREDEFINED_LANES

    lanes, lane_polygons = load_lane_polygons(mock_lanes_file)
    assert len(lanes) == 2
    assert isinstance(lane_polygons["1"], np.ndarray)
    assert lane_polygons["1"].shape == (4, 2)


def test_draw_vehicle_annotations():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    tracking_data = [(1, [10, 10, 20, 20], "car")]
    result = draw_vehicle_annotations(frame.copy(), tracking_data)
    assert result.shape == frame.shape


def test_update_lane_metrics():
    polygon = np.array([[0, 0], [100, 0], [100, 100], [0, 100]], dtype=np.int32)
    lane_polygons = {"1": polygon}
    tracking_data = [(1, [10, 10, 20, 20], "car")]

    entries = {"1": set()}
    counts = {"1": 0}
    labels = {"1": []}
    occupancy = defaultdict(int)
    vehicle_timestamps = {"1": []}

    update_lane_metrics(
        tracking_data,
        lane_polygons,
        entries,
        counts,
        labels,
        occupancy,
        vehicle_timestamps,
    )

    assert 1 in entries["1"]
    assert counts["1"] == 1
    assert labels["1"] == ["car"]
    assert occupancy["1"] == 1
    assert len(vehicle_timestamps["1"]) == 1
    assert isinstance(vehicle_timestamps["1"][0], datetime)


def test_draw_lane_counters():
    frame = np.zeros((200, 200, 3), dtype=np.uint8)
    lanes = [{"id": "1", "label": "Left", "direction": "North"}]
    counts = {"1": 5}
    result = draw_lane_counters(frame.copy(), lanes, counts)
    assert result.shape == frame.shape


@pytest.mark.asyncio
async def test_stream_frame():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    payload = {"frame": frame}
    mock_websocket = mock.AsyncMock()
    await stream_frame(mock_websocket, payload)
    assert mock_websocket.send_text.called
    args = mock_websocket.send_text.call_args[0]
    assert "frame" in json.loads(args[0])
