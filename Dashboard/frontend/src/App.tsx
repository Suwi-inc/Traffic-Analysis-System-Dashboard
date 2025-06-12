import VideoMetrics from "./components/VideoMetrics";
import VideoPlayer from "./components/VideoPlayer";
import Header from "./components/Header";
import Uploader from "./components/Uploader";
import History from "./components/History";

const App = () => {
  return (
    <>
      <Header />
      <div className="pt-5 font-sans min-w-[600px] flex justify-center w-full flex-col gap-4">
        <Uploader />
        <VideoPlayer />
      </div>
      <div className="flex flex-col w-full justify-between">
        <VideoMetrics />
        <History />
      </div>
    </>
  );
};

export default App;
