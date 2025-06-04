from fastapi.testclient import TestClient
from ..app import app
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


client = TestClient(app)


def test_upload_video_success(tmp_path):
    video_path = tmp_path / "test_video.mp4"
    video_path.write_bytes(b"test video content")

    with open(video_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test_video.mp4", f, "video/mp4")},
            data={"counter": "1", "show_lanes": "1", "vehicles": "1"},
        )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["filename"] == "test_video.mp4"
    assert response_data["temp_path"].endswith(".mp4")


def test_upload_video_invalid_file_type(tmp_path):
    fake_file = tmp_path / "not_a_video.txt"
    fake_file.write_text("Just some text")

    with open(fake_file, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("not_a_video.txt", f, "text/plain")},
            data={"counter": "1", "show_lanes": "1", "vehicles": "1"},
        )

    assert response.status_code == 400
