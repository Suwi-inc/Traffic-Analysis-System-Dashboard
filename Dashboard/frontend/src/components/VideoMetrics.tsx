import Fps from "./Fps";
import { useAtomValue } from "jotai";
import { resultAtom } from "../atoms";
import Occupancy from "./Occupancy";
import TypeDistribution from "./TypeDistribution";

const VideoMetrics = () => {
  const result = useAtomValue(resultAtom);

  if (result === null) {
    return;
  }

  return (
    <div className="w-full mx-auto flex flex-col items-center p-8 gap-4">
      <h3 className="mb-2.5 pb-2.5 border-b-1 border-b-black border-solid text-center text-2xl font-semibold">
        Video Metrics
      </h3>
      <div className="flex flex-wrap gap-8 h-fit items-start justify-center">
        <Fps value={`${result.fps.toFixed(2)}`} />
        <Occupancy
          lane1={`${result.occupancy.lane_1}`}
          lane2={`${result.occupancy.lane_2}`}
        />
        <TypeDistribution
          lane1={result.type_distribution.lane_1}
          lane2={result.type_distribution.lane_2}
        />
        {/* <Card title="Resolution" item={`${metrics.resolution}`} /> */}
        {/* <Card title="Latency" item={`${metrics.latency}`} /> */}
        {/* <Card title="Objects Detected" item={`${metrics.objects}`} /> */}
      </div>
    </div>
  );
};

export default VideoMetrics;
