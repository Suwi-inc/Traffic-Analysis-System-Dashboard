export interface Result {
  frame: string;
  type_distribution: {
    [key: string]: {
      [key: string]: number;
    };
  };
  occupancy: {
    [key: string]: number;
  };
  counts_per_minute: {
    [key: string]: {
      [key: string]: number;
    };
  };
  counts_per_hour: {
    [key: string]: {
      [key: string]: number;
    };
  };
  fps: number;
}

export interface HistoryResult {
  metrics: [
    {
      metric_id: number;
      video_name: string;
      time: string;
      lane_occupancy: [
        {
          lane_name: string;
          occupancy_rate: number;
        }
      ];
      vehicle_distribution: [
        {
          lane_name: string;
          car: number;
          truck: number;
          motorcycle: number;
          bus: number;
          other: number;
        }
      ];
      vehicle_counts: [];
    }
  ];
}
