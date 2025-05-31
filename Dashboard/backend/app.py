from typing import Annotated
from fastapi import (
    FastAPI,
    Form,
    UploadFile,
    File,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from fastapi.responses import JSONResponse
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
    if not file.content_type.startswith("video/"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid file type. Only video files are allowed."},
        )
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
    except WebSocketDisconnect:
        print("WebSocket disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.discard(websocket)


@app.on_event("shutdown")
async def cleanup():
    global current_video_path
    if current_video_path and os.path.exists(current_video_path):
        os.unlink(current_video_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
