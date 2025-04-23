import { useState, useEffect } from "react";

interface Prop {
  isStreaming: boolean;
}

const VideoMetrics = ({ isStreaming }: Prop) => {
  const [metrics, setMetrics] = useState({
    fps: 0,
    resolution: "0x0",
    bitrate: "0 kbps",
    latency: "0 ms",
    objects: 0,
    timestamp: new Date().toLocaleTimeString(),
  });

  useEffect(() => {
    if (!isStreaming) {
      setMetrics({
        fps: 0,
        resolution: "0x0",
        bitrate: "0 kbps",
        latency: "0 ms",
        objects: 0,
        timestamp: "--:--:--",
      });
      return;
    }

    // Simulate changing metrics while streaming
    const interval = setInterval(() => {
      setMetrics({
        fps: Math.floor(Math.random() * 30) + 15, // 15-45 FPS
        resolution: `${Math.floor(Math.random() * 500) + 720}x${
          Math.floor(Math.random() * 300) + 480
        }`,
        bitrate: `${Math.floor(Math.random() * 4000) + 1000} kbps`,
        latency: `${Math.floor(Math.random() * 100) + 50} ms`,
        objects: Math.floor(Math.random() * 10),
        timestamp: new Date().toLocaleTimeString(),
      });
    }, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, [isStreaming]);

  return (
    <div className="bg-gray-300 text-black p-4 rounded w-80 h-fit ml-2.5 mt-12">
      <h3 className="mt-0 mb-2.5 pb-2.5 border-b-1 border-b-black border-solid text-center">
        Video Metrics
      </h3>
      <div className="grid grid-cols-[1fr] gap-2.5">
        <div className="flex justify-between items-center">
          <span className="font-semibold text-black">FPS:</span>
          <span className="font-mono text-black">{metrics.fps}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="font-semibold text-black">Resolution:</span>
          <span className="font-mono text-black">{metrics.resolution}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="font-semibold text-black">Bitrate:</span>
          <span className="font-mono text-black">{metrics.bitrate}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="font-semibold text-black">Latency:</span>
          <span className="font-mono text-black">{metrics.latency}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="font-semibold text-black">Objects Detected:</span>
          <span className="font-mono text-black">{metrics.objects}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="font-semibold text-black">Last Update:</span>
          <span className="font-mono text-black">{metrics.timestamp}</span>
        </div>
      </div>
    </div>
  );
};

export default VideoMetrics;
