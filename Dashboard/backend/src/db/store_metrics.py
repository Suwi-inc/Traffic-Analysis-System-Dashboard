from sqlalchemy.orm import Session
from .db_model import Metrics, LaneOccupancy, VehicleDistribution
from datetime import datetime, timezone


def store_metrics_data(
    db: Session,
    video_name,
    type_distribution: dict,
    occupancy: dict,
):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    video_name = f"{video_name}_{timestamp}"
    metric = Metrics(video_name=video_name)
    db.add(metric)
    db.flush()

    for lane_id, occ_rate in occupancy.items():
        db.add(
            LaneOccupancy(
                metrics_id=metric.metric_id,
                lane_name=lane_id,
                occupancy_rate=occ_rate,
            )
        )

    for lane_id, dist in type_distribution.items():
        db.add(
            VehicleDistribution(
                metrics_id=metric.metric_id,
                lane_name=lane_id,
                car=dist.get("car", 0),
                truck=dist.get("truck", 0),
                motorcycle=dist.get("motorcycle", 0),
                bus=dist.get("bus", 0),
                other=dist.get("other", 0),
            )
        )

    """ for lane_name, count in counts_per_minute.items():
        db.add(
            VehicleCounts(
                metrics_id=metric.metric_id,
                lane_name=lane_name,
                count_minute=count,
                count_hour=counts_per_hour.get(lane_name, 0),
            )
        ) """

    db.commit()
