import { useState } from "react";
import VideoMetrics from "./components/VideoMetrics";
import VideoPlayer from "./components/VideoPlayer";
import Header from "./components/Header";

const App = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  return (
    <>
      <Header />
      <div className="pt-5 font-sans min-w-[600px] flex justify-center">
        <VideoPlayer onStreamingChange={setIsStreaming} />
      </div>
      <div className="flex min-w-[600px] justify-center">
        <VideoMetrics isStreaming={isStreaming} />
      </div>
    </>
  );
};

export default App;
