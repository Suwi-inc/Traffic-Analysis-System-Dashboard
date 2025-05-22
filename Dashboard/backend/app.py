import asyncio
from typing import Annotated
from fastapi import FastAPI, Form, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import tempfile
import os
from random import Random
from datetime import datetime
from time import time
from src.process_and_stream_analysis import process_and_stream_analysis


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store video path
current_video_path = None
current_show = {}
connected_clients = set()


@app.post("/upload")
async def upload_video(
    counter: Annotated[str, Form()],
    show_lanes: Annotated[str, Form()],
    vehicles: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    global current_video_path
    global current_show
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        contents = await file.read()
        tmp_file.write(contents)
        current_video_path = tmp_file.name
    current_show = {"vehicles": vehicles, "counter": counter, "show_lanes": show_lanes}

    return {"filename": file.filename, "temp_path": current_video_path}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "start_stream":
                await process_and_stream_analysis(
                    websocket,
                    current_video_path,
                    current_show["vehicles"] == "1",
                    current_show["counter"] == "1",
                    current_show["show_lanes"] == "1",
                )
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.discard(websocket)


@app.websocket("/metrics")
async def metrics_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "stream_metrics":
                await send_metrics(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.discard(websocket)


async def send_metrics(websocket: WebSocket):
    while True:
        rand = Random()
        fps = rand.randint(15, 45)
        resolution = f"{rand.randint(640, 1920)}x{rand.randint(480, 1080)}"
        bitrate = f"{rand.randint(999, 4999)} kbps"
        latency = f"{rand.randint(0, 200)} ms"
        objects = rand.randint(0, 9)
        timestamp = f"{datetime.fromtimestamp(time()).time().strftime('%H:%M:%S')}"
        message = json.dumps(
            {
                "fps": fps,
                "resolution": resolution,
                "bitrate": bitrate,
                "latency": latency,
                "objects": objects,
                "timestamp": timestamp,
            }
        )
        await websocket.send_text(message)
        await asyncio.sleep(0.5)


@app.on_event("shutdown")
async def cleanup():
    global current_video_path
    if current_video_path and os.path.exists(current_video_path):
        os.unlink(current_video_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
