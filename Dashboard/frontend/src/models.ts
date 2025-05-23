export interface Result {
  frame: string;
  type_distribution: {
    lane_1: {
      [key: string]: number;
    };
    lane_2: {
      [key: string]: number;
    };
  };
  occupancy: {
    lane_1: number;
    lane_2: number;
  };
  counts_per_minute: {
    lane_1: {
      [key: string]: number;
    };
    lane_2: {
      [key: string]: number;
    };
  };
  counts_per_hour: {
    lane_1: {
      [key: string]: number;
    };
    lane_2: {
      [key: string]: number;
    };
  };
  fps: number;
}
