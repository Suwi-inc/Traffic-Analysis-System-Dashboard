import { useState } from "react";
import VideoMetrics from "./components/VideoMetrics";
import VideoPlayer from "./components/VideoPlayer";
import Header from "./components/Header";

const App = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  return (
    <div className="h-screen">
      <Header />
      <div className="flex h-full p-[100px] box-border bg-white justify-center g-[100px]">
        <VideoMetrics isStreaming={isStreaming} />
        <div className="text-center self-stretch p-5 font-sans">
          <VideoPlayer onStreamingChange={setIsStreaming} />
        </div>
        <VideoMetrics isStreaming={isStreaming} />
      </div>
    </div>
  );
};

export default App;
