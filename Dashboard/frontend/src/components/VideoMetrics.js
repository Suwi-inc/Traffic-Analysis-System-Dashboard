import React, { useState, useEffect } from 'react';
import '../styles/Metrics.css'; 

const VideoMetrics = ({ isStreaming }) => {
  const [metrics, setMetrics] = useState({
    fps: 0,
    resolution: '0x0',
    bitrate: '0 kbps',
    latency: '0 ms',
    objects: 0,
    timestamp: new Date().toLocaleTimeString()
  });

  useEffect(() => {
    if (!isStreaming) {
      setMetrics({
        fps: 0,
        resolution: '0x0',
        bitrate: '0 kbps',
        latency: '0 ms',
        objects: 0,
        timestamp: '--:--:--'
      });
      return;
    }

    // Simulate changing metrics while streaming
    const interval = setInterval(() => {
      setMetrics({
        fps: Math.floor(Math.random() * 30) + 15, // 15-45 FPS
        resolution: `${Math.floor(Math.random() * 500) + 720}x${Math.floor(Math.random() * 300) + 480}`,
        bitrate: `${Math.floor(Math.random() * 4000) + 1000} kbps`,
        latency: `${Math.floor(Math.random() * 100) + 50} ms`,
        objects: Math.floor(Math.random() * 10),
        timestamp: new Date().toLocaleTimeString()
      });
    }, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, [isStreaming]);

  return (
    <div className="metrics-panel">
      <h3>Video Metrics</h3>
      <div className="metrics-grid">
        <div className="metric-item">
          <span className="metric-label">FPS:</span>
          <span className="metric-value">{metrics.fps}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Resolution:</span>
          <span className="metric-value">{metrics.resolution}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Bitrate:</span>
          <span className="metric-value">{metrics.bitrate}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Latency:</span>
          <span className="metric-value">{metrics.latency}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Objects Detected:</span>
          <span className="metric-value">{metrics.objects}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Last Update:</span>
          <span className="metric-value">{metrics.timestamp}</span>
        </div>
      </div>
    </div>
  );
};

export default VideoMetrics;