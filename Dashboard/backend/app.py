import asyncio
import cv2
import numpy as np
import websockets
from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import base64
import tempfile
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store video path
current_video_path = None
connected_clients = set()

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    global current_video_path
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        contents = await file.read()
        tmp_file.write(contents)
        current_video_path = tmp_file.name
    
    return {"filename": file.filename, "temp_path": current_video_path}

async def process_and_stream_video(websocket):
    global current_video_path
    try:
        if current_video_path and os.path.exists(current_video_path):
            video = cv2.VideoCapture(current_video_path)
            
            while video.isOpened():
                success, frame = video.read()
                if not success:
                    break
                
                # Convert frame to JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                
                # Send frame to client
                message = json.dumps({'frame': jpg_as_text})
                await websocket.send_text(message)
                
                # Control frame rate (~30fps)
                await asyncio.sleep(0.033)
            
            video.release()
            # Clean up temporary file
            os.unlink(current_video_path)
            current_video_path = None
            
    except Exception as e:
        print(f"Streaming error: {e}")
        if current_video_path and os.path.exists(current_video_path):
            os.unlink(current_video_path)
            current_video_path = None
    finally:
        connected_clients.discard(websocket)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "start_stream":
                await process_and_stream_video(websocket)
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