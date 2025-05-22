import VideoMetrics from "./components/VideoMetrics";
import VideoPlayer from "./components/VideoPlayer";
import Header from "./components/Header";
import Uploader from "./components/Uploader";

const App = () => {
  return (
    <>
      <Header />
      <div className="pt-5 font-sans min-w-[600px] flex justify-center w-full flex-col gap-4">
        <Uploader />
        <VideoPlayer />
      </div>
      <div className="flex min-w-[600px] justify-center">
        <VideoMetrics />
      </div>
    </>
  );
};

export default App;
