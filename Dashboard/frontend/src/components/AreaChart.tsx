import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export interface BitRateData {
  xaxis: string;
  area: string;
}

interface Props {
  timestamp: string;
  bitrate: string;
}

const BitRateAreaChart = ({ timestamp, bitrate }: Props) => {
  const [data, setData] = useState<BitRateData[]>([]);
  useEffect(() => {
    if (data.length >= 10) {
      setData((x) =>
        [...x, { xaxis: timestamp, area: bitrate }].slice(-10, -1)
      );
    } else {
      setData((x) => [...x, { xaxis: timestamp, area: bitrate }]);
    }
  }, [bitrate]);
  return (
    <div>
      <AreaChart
        width={900}
        height={400}
        data={data}
        margin={{
          top: 10,
          right: 30,
          left: 0,
          bottom: 0,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="xaxis" />
        <YAxis />
        <Tooltip />
        <Area type="monotone" dataKey="area" stroke="#8884d8" fill="#8884d8" />
      </AreaChart>
      <div className="font-semibold text-black text-3xl text-center">
        Bitrate
      </div>
    </div>
  );
};

export default BitRateAreaChart;
