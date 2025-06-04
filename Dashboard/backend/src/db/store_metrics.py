from sqlalchemy.orm import Session, joinedload
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


def retrieve_metrics_data(db: Session):
    metrics_data = []
    metrics_records = (
        db.query(Metrics)
        .options(
            joinedload(Metrics.lane_occupancy),
            joinedload(Metrics.vehicle_distribution),
            joinedload(Metrics.vehicle_counts),
        )
        .all()
    )

    for metric in metrics_records:
        data = {
            "metric_id": metric.metric_id,
            "video_name": metric.video_name,
            "time": metric.time.isoformat(),
            "lane_occupancy": [],
            "vehicle_distribution": [],
            "vehicle_counts": [],
        }

        for occ in metric.lane_occupancy:
            data["lane_occupancy"].append(
                {"lane_name": occ.lane_name, "occupancy_rate": occ.occupancy_rate}
            )

        for dist in metric.vehicle_distribution:
            data["vehicle_distribution"].append(
                {
                    "lane_name": dist.lane_name,
                    "car": dist.car,
                    "truck": dist.truck,
                    "motorcycle": dist.motorcycle,
                    "bus": dist.bus,
                    "other": dist.other,
                }
            )

        """  for count in metric.vehicle_counts:
                data["vehicle_counts"].append(
                    {
                        "lane_name": count.lane_name,
                        "count_minute": count.count_minute,
                        "count_hour": count.count_hour,
                    }
                ) """

        metrics_data.append(data)

    return metrics_data
