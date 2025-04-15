import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Styles.css';

const VideoPlayer = ({ onStreamingChange }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const videoRef = useRef(null);
  const [message, setMessage] = useState('');
  const ws = useRef(null);

  // Get endpoints from environment variables
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
  const WS_BASE_URL = process.env.REACT_APP_WS_BASE_URL;

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      setMessage('Uploading...');
      await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage('Video uploaded successfully!');
    } catch (error) {
      setMessage('Error uploading video');
      console.error('Error:', error);
    }
  };

  const startStream = () => {
    if (!selectedFile) {
      setMessage('Please upload a video first!');
      return;
    }

    setIsStreaming(true);
    setMessage('Starting stream...');

    // Use environment variable for WebSocket URL
    ws.current = new WebSocket(`${WS_BASE_URL}/ws`);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      ws.current.send('start_stream');
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.frame && videoRef.current) {
          videoRef.current.src = `data:image/jpeg;base64,${data.frame}`;
        }
      } catch (error) {
        console.error('Error processing frame:', error);
      }
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setMessage('Streaming error occurred');
      setIsStreaming(false);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
      setIsStreaming(false);
    };
    if (onStreamingChange) onStreamingChange(true);
  };

  const stopStream = () => {
    if (ws.current) {
      ws.current.close();
    }
    setIsStreaming(false);
    setMessage('Stream stopped');
    if (onStreamingChange) onStreamingChange(false);
  };

  return (
    <div className="video-container">
      <h2>Video Streaming Dashboard</h2>
      
      <div className="upload-section">
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload Video</button>
        {message && <p>{message}</p>}
      </div>
      
      <div className="stream-section">
        <button 
          onClick={isStreaming ? stopStream : startStream}
          disabled={!selectedFile}
        >
          {isStreaming ? 'Stop Stream' : 'Start Stream'}
        </button>
        
        <div className="video-wrapper">
          {isStreaming ? (
            <img 
              ref={videoRef} 
              alt="Video Stream" 
              style={{ maxWidth: '100%', maxHeight: '500px' }}
            />
          ) : (
            <p>Stream will appear here when started</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;