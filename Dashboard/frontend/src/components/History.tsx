import { useAtomValue } from "jotai";
import { isStreamingAtom } from "../atoms";
import { useEffect, useState } from "react";
import { HistoryResult } from "../models";
import relativeTime from "dayjs/plugin/relativeTime";
import dayjs from "dayjs";

dayjs.extend(relativeTime);

const History = () => {
  const isStreaming = useAtomValue(isStreamingAtom);
  const [history, setHistory] = useState<HistoryResult | null>(null);

  useEffect(() => {
    if (!isStreaming) {
      const url = import.meta.env.VITE_APP_API_BASE_URL as string;
      fetch(`${url}/metrics`).then(async (x) => setHistory(await x.json()));
    }
  }, [isStreaming]);

  return (
    <div className="w-full mx-auto flex flex-col items-center p-8 gap-4">
      <h3 className="mb-2.5 pb-2.5 border-b-1 border-b-black border-solid text-center text-2xl font-semibold">
        History
      </h3>
      {!history && <>No history yet, please upload a video and start stream </>}
      {history && (
        <table className="table-auto w-full border-collapse border border-gray-400 border-spacing-2">
          <thead>
            <tr>
              <th className="border border-gray-300">Video Name</th>
              <th className="border border-gray-300">Time</th>
              <th className="border border-gray-300">Lane Occupancy</th>
              <th className="border border-gray-300">Vehicle Distribution</th>
            </tr>
          </thead>
          <tbody>
            {history.metrics
              .sort((x, y) => y.metric_id - x.metric_id)
              .map((x) => (
                <tr key={x.metric_id} className="text-center">
                  <td className="border border-gray-300">
                    {x.video_name.split(".mp4")[0]}
                  </td>
                  <td className="border border-gray-300">
                    {dayjs(x.time).fromNow()}
                  </td>
                  <td className="border border-gray-300">
                    <table className="table-fixed">
                      <thead>
                        <tr>
                          <th>Lane Name</th>
                          <th>Occupancy Rate</th>
                        </tr>
                      </thead>
                      <tbody>
                        {x.lane_occupancy.map((y) => (
                          <tr key={y.occupancy_rate} className="text-center">
                            <td>{y.lane_name}</td>
                            <td>{y.occupancy_rate}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </td>
                  <td className="border border-gray-300">
                    <table className="table-fixed">
                      <thead>
                        <tr>
                          <th>Lane Name</th>
                          <th>Car</th>
                          <th>Truck</th>
                          <th>Motorcycle</th>
                          <th>Bus</th>
                          <th>Other</th>
                        </tr>
                      </thead>
                      <tbody>
                        {x.vehicle_distribution.map((y) => (
                          <tr key={y.car} className="text-center">
                            <td>{y.lane_name}</td>
                            <td>{y.car}</td>
                            <td>{y.truck}</td>
                            <td>{y.motorcycle}</td>
                            <td>{y.bus}</td>
                            <td>{y.other}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default History;
