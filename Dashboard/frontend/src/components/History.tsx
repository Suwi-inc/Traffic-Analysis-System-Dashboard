import { useAtomValue } from "jotai";
import { isStreamingAtom } from "../atoms";
import { useEffect, useState } from "react";
import { HistoryResult } from "../models";

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
      <h3 className="mb-2.5 pb-2.5 border-b border-black text-center text-2xl font-semibold">
        History
      </h3>
      {!history && <>No history yet, please upload a video and start stream</>}
      {history && (
        <table className="table-auto w-full border-collapse border border-gray-400 shadow-2xl text-sm text-center">
          <thead>
            <tr>
              <th rowSpan={2} className="border border-gray-300">
                Video Name
              </th>
              <th rowSpan={2} className="border border-gray-300">
                Time
              </th>
              <th colSpan={2} className="border border-gray-300">
                Lane Occupancy
              </th>
              <th colSpan={6} className="border border-gray-300">
                Vehicle Distribution
              </th>
            </tr>
            <tr>
              <th className="border border-gray-300">Lane</th>
              <th className="border border-gray-300">Occupancy Rate</th>
              <th className="border border-gray-300">Lane</th>
              <th className="border border-gray-300">Car</th>
              <th className="border border-gray-300">Truck</th>
              <th className="border border-gray-300">Motorcycle</th>
              <th className="border border-gray-300">Bus</th>
              <th className="border border-gray-300">Other</th>
            </tr>
          </thead>
          <tbody>
            {history.metrics
              .sort((a, b) => b.metric_id - a.metric_id)
              .map((metric) => {
                const maxRows = Math.max(
                  metric.lane_occupancy.length,
                  metric.vehicle_distribution.length
                );

                return [...Array(maxRows)].map((_, rowIndex) => {
                  const occ = metric.lane_occupancy[rowIndex];
                  const veh = metric.vehicle_distribution[rowIndex];

                  return (
                    <tr key={`${metric.metric_id}-${rowIndex}`}>
                      {rowIndex === 0 && (
                        <>
                          <td
                            rowSpan={maxRows}
                            className="border border-gray-300"
                          >
                            {metric.video_name}
                          </td>
                          <td
                            rowSpan={maxRows}
                            className="border border-gray-300"
                          >
                            {new Date(metric.time).toLocaleString()}
                          </td>
                        </>
                      )}
                      <td className="border border-gray-300">
                        {occ?.lane_name || ""}
                      </td>
                      <td className="border border-gray-300">
                        {occ?.occupancy_rate ?? ""}
                      </td>
                      <td className="border border-gray-300">
                        {veh?.lane_name || ""}
                      </td>
                      <td className="border border-gray-300">
                        {veh?.car ?? ""}
                      </td>
                      <td className="border border-gray-300">
                        {veh?.truck ?? ""}
                      </td>
                      <td className="border border-gray-300">
                        {veh?.motorcycle ?? ""}
                      </td>
                      <td className="border border-gray-300">
                        {veh?.bus ?? ""}
                      </td>
                      <td className="border border-gray-300">
                        {veh?.other ?? ""}
                      </td>
                    </tr>
                  );
                });
              })}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default History;
