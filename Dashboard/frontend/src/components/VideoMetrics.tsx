import { useState, useEffect, useRef } from "react";
import Card from "./Card";
import BitRateAreaChart from "./AreaChart";

interface Prop {
  isStreaming: boolean;
}

interface Metrics {
  fps: number;
  resolution: string;
  bitrate: string;
  latency: string;
  objects: number;
  timestamp: string;
}

const VideoMetrics = ({ isStreaming }: Prop) => {
  const ws = useRef<WebSocket>(null);
  const [metrics, setMetrics] = useState<Metrics>({
    fps: 0,
    resolution: "0x0",
    bitrate: "0 kbps",
    latency: "0 ms",
    objects: 0,
    timestamp: new Date().toLocaleTimeString(),
  });

  useEffect(() => {
    if (isStreaming) {
      startStream();
    } else {
      stopStream();
    }
  }, [isStreaming]);

  const WS_BASE_URL = import.meta.env.VITE_APP_WS_BASE_URL;

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const startStream = () => {
    ws.current = new WebSocket(`${WS_BASE_URL}/metrics`);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
      ws.current?.send("stream_metrics");
    };

    ws.current.onmessage = (event) => {
      try {
        const data: Metrics = JSON.parse(event.data);
        setMetrics(data);
      } catch (error) {
        console.error("Error processing frame:", error);
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
    };
  };

  const stopStream = () => {
    if (!isStreaming && ws.current) {
      ws.current.close();
    }
  };

  return (
    <div className="w-full mx-auto flex flex-col items-center p-8 gap-4">
      <h3 className="mb-2.5 pb-2.5 border-b-1 border-b-black border-solid text-center text-2xl font-semibold">
        Video Metrics
      </h3>
      <div className="flex flex-wrap gap-8 h-fit justify-center">
        <Card title="FPS" item={`${metrics.fps}`} />
        <Card title="Resolution" item={`${metrics.resolution}`} />
        <Card title="Latency" item={`${metrics.latency}`} />
        <Card title="Objects Detected" item={`${metrics.objects}`} />
      </div>
      <BitRateAreaChart
        timestamp={`${metrics.timestamp}`}
        bitrate={`${metrics.bitrate.split(" kbps")[0]}`}
      />
    </div>
  );
};

export default VideoMetrics;
