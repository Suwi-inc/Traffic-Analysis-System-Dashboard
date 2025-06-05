import Fps from "./Fps";
import { useAtomValue } from "jotai";
import { resultAtom } from "../atoms";
import Occupancy from "./Occupancy";
import TypeDistribution from "./TypeDistribution";

const VideoMetrics = () => {
  const result = useAtomValue(resultAtom);

  if (result === null) {
    return (
      <div className="w-full mx-auto flex flex-col items-center p-8 gap-4 font-bold text-2xl">
        Upload a video and start stream to see metrics
      </div>
    );
  }

  return (
    <div className="w-full mx-auto flex flex-col items-center p-8 gap-4">
      <h3 className="mb-2.5 pb-2.5 border-b-1 border-b-black border-solid text-center text-2xl font-semibold">
        Video Metrics
      </h3>
      <div className="flex flex-wrap gap-8 h-fit items-start justify-start">
        <Fps value={`${result.fps.toFixed(2)}`} />
        <Occupancy occupancy={result.occupancy} />
        <TypeDistribution type_distribution={result.type_distribution} />
      </div>
    </div>
  );
};

export default VideoMetrics;
