import { useRef, useEffect, useState } from "react";
import { useAtomValue, useSetAtom } from "jotai";
import {
  messageAtom,
  isUploadedAtom,
  resultAtom,
} from "../atoms";
import { Result } from "../models";

const VideoPlayer = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const isUploaded = useAtomValue(isUploadedAtom);
  const setMessage = useSetAtom(messageAtom);
  const setResult = useSetAtom(resultAtom);
  const videoRef = useRef<HTMLImageElement | null>(null);
  const ws = useRef<WebSocket | null>(null);

  const WS_BASE_URL = import.meta.env.VITE_APP_WS_BASE_URL;

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const startStream = () => {
    if (!isUploaded) {
      setMessage("Please upload a video first!");
      return;
    }

    setIsStreaming(true);
    setMessage("Starting stream...");

    ws.current = new WebSocket(`${WS_BASE_URL}/ws`);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
      ws.current?.send("start_stream");
    };

    ws.current.onmessage = (event) => {
      try {
        const data: Result = JSON.parse(event.data);
        setResult(data);
        if (data.frame && videoRef.current) {
          videoRef.current.src = `data:image/jpeg;base64,${data.frame}`;
        }
      } catch (error) {
        console.error("Error processing frame:", error);
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
      setMessage("Streaming error occurred");
      setIsStreaming(false);
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
      setIsStreaming(false);
    };
    if (setIsStreaming) setIsStreaming(true);
  };

  const stopStream = () => {
    if (ws.current) {
      ws.current.close();
    }
    setIsStreaming(false);
    setMessage("Stream stopped");
    if (setIsStreaming) setIsStreaming(false);
  };

  return (
    <div className="p-2.5 border-solid border-1 border-gray-200 rounded-lg bg-white">
      <h2 className="text-lg text-center font-semibold">
        Video Streaming Dashboard
      </h2>
      <div className="p-4 bg-white text-center rounded-md shadow-md">
        <button
          className="px-4 py-2 mx-1.5 bg-green-600 text-white border-none rounded-sm cursor-pointer hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          onClick={isStreaming ? stopStream : startStream}
          disabled={!isUploaded}
        >
          {isStreaming ? "Stop Stream" : "Start Stream"}
        </button>
        <div className="mt-3.5 min-h-80 flex items-center justify-center bg-white rounded-md">
          {isStreaming ? (
            <img
              ref={videoRef}
              alt="Video Stream"
              style={{ maxWidth: "100%", maxHeight: "500px" }}
            />
          ) : (
            <p className="text-center">Stream will appear here when started</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
