import React, { useState } from 'react';
import VideoPlayer from './components/VideoPlayer';
import VideoMetrics from './components/VideoMetrics';
import './styles/App.css'; 


function App() {
  const [isStreaming, setIsStreaming] = useState(false);
  return (
    <div className='App'>
       <div className='metrics-panel'>
       <VideoMetrics isStreaming={isStreaming} />
      </div>
      <div  className="Video">
      <VideoPlayer onStreamingChange={setIsStreaming} />
      </div>
      <div className='metrics-panel'>
       <VideoMetrics isStreaming={isStreaming} />
      </div>
    </div>
  );
}

export default App;